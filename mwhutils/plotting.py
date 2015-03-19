"""
Plotting for various models.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as pl

__all__ = []


class axis(object):
    def __init__(self, ax):
        self.ax = ax

    def set_title(self, title):
        self.ax.set_title(title)

    def set_xlabel(self, xlabel):
        self.ax.set_xlabel(xlabel)

    def set_ylabel(self, xlabel):
        self.ax.set_xlabel(xlabel)

    def set_lim(self, xmin=None, xmax=None, ymin=None, ymax=None):
        xmin, xmax, ymin, ymax = self.get_lim(xmin, xmax, ymin, ymax)
        self.ax.axis((xmin, xmax, ymin, ymax))

    def get_lim(self, xmin=None, xmax=None, ymin=None, ymax=None):
        xmin_, xmax_, ymin_, ymax_ = self.ax.axis()
        xmin = xmin if (xmin is None) else min(xmin, xmin_)
        xmax = xmax if (xmax is None) else max(xmax, xmax_)
        ymin = ymin if (ymin is None) else min(ymin, ymin_)
        ymax = ymax if (ymax is None) else max(ymax, ymax_)
        return xmin, xmax, ymin, ymax

    def remove_ticks(self, xticks=True, yticks=True):
        if xticks:
            self.ax.set_xticklabels([])
        if yticks:
            self.ax.set_yticklabels([])

    def plot(self, x, y, **kwargs):
        self.ax.plot(x, y, **kwargs)

    def plot_banded(self, x, y, lo=None, hi=None):
        lo = np.zeros_like(y) if (lo is None) else lo
        hi = y if (hi is None) else hi
        lines = self.ax.plot(x, y)
        color = lines[0].get_color()
        alpha = 0.25
        self.ax.fill_between(x, lo, hi, color=color, alpha=alpha)

    def scatter(self, x, y):
        self.ax.scatter(x, y, marker='o', s=30, lw=1, facecolors='none')

    def vline(self, x):
        self.ax.axvline(x, ls='--', color='r')

    def hline(self, y):
        self.ax.axhline(y, ls='--', color='r')

    def draw(self):
        self.ax.axis('tight')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)


class figure(object):
    def __init__(self, fig=None, rows=1, cols=1):
        if fig is None:
            fig = pl.figure()
        elif isinstance(fig, int):
            fig = pl.figure(fig)
        elif not isinstance(fig, pl.Figure):
            raise ValueError('fig must be a Figure instance or an integer')
        self._fig = fig
        self._fig.clf()
        self._rows = rows
        self._cols = cols
        self._subplots = [None for _ in xrange(rows*cols)]

    def __getitem__(self, a):
        if self._rows == 1 or self._cols == 1:
            if not isinstance(a, int):
                raise ValueError('single row/column figures can only be '
                                 'indexed by an integer')
        else:
            if not isinstance(a, tuple) or len(a) != 2:
                raise ValueError('grid-based figures must be indexed by '
                                 'two integers')
            a = self._cols * a[0] + a[1]
        ax = self._subplots[a]
        if ax is None:
            ax = axis(self._fig.add_subplot(self._rows, self._cols, a+1))
            self._subplots[a] = ax
        return ax

    def draw(self):
        for ax in self._subplots:
            if ax is not None:
                ax.draw()

        for x in xrange(self._rows):
            ymin, ymax, axes = np.inf, -np.inf, []
            for y in xrange(self._cols):
                ax = self._subplots[self._cols * x + y]
                if ax is not None:
                    axes.append(ax)
                    ymin, ymax = ax.get_lim(ymin=ymin, ymax=ymax)[2:]
            for ax in axes:
                ax.set_lim(ymin=ymin, ymax=ymax)
            for ax in axes[1:]:
                ax.remove_ticks(xticks=False)

        for y in xrange(self._cols):
            xmin, xmax, axes = np.inf, -np.inf, []
            for x in xrange(self._rows):
                ax = self._subplots[self._cols * x + y]
                if ax is not None:
                    axes.append(ax)
                    xmin, xmax = ax.get_lim(xmin=xmin, xmax=xmax)[:2]
            for ax in axes:
                ax.set_lim(xmin=xmin, xmax=xmax)
            for ax in axes[0:-1]:
                ax.remove_ticks(yticks=False)

        self._fig.canvas.draw()
        pl.show(block=False)
