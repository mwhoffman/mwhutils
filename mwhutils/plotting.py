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

    def get_ylim(self, ymin_=None, ymax_=None):
        ymin, ymax = self.ax.axis()[2:4]
        if ymin_ is not None:
            ymin = min(ymin, ymin_)
        if ymax_ is not None:
            ymax = max(ymax, ymax_)
        return ymin, ymax

    def set_ylim(self, ymin=None, ymax=None):
        ymin, ymax = self.get_ylim(ymin, ymax)
        self.ax.axis(ymin=ymin, ymax=ymax)

    def get_xlim(self, xmin_=None, xmax_=None):
        xmin, xmax = self.ax.axis()[0:2]
        if xmin_ is not None:
            xmin = min(xmin, xmin_)
        if xmax_ is not None:
            xmax = max(xmax, xmax_)
        return xmin, xmax

    def set_xlim(self, xmin=None, xmax=None):
        xmin, xmax = self.get_xlim(xmin, xmax)
        self.ax.axis(xmin=xmin, xmax=xmax)

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
        self.fig = fig
        self.fig.clf()
        self.rows = rows
        self.cols = cols
        self.subplots = [None for _ in xrange(rows*cols)]

    def __getitem__(self, a):
        if self.rows == 1 or self.cols == 1:
            if not isinstance(a, int):
                raise ValueError('single row/column figures can only be '
                                 'indexed by an integer')
        else:
            if not isinstance(a, tuple) or len(a) != 2:
                raise ValueError('grid-based figures must be indexed by '
                                 'two integers')
            a = self.cols * a[0] + a[1]
        ax = self.subplots[a]
        if ax is None:
            ax = axis(self.fig.add_subplot(self.rows, self.cols, a+1))
            self.subplots[a] = ax
        return ax

    def remove_ticks(self):
        for ax in self.subplots:
            if ax is not None:
                ax.remove_ticks()

    def draw(self):
        for ax in self.subplots:
            if ax is not None:
                ax.draw()

        for x in xrange(self.rows):
            ymin, ymax, axes = np.inf, -np.inf, []
            for y in xrange(self.cols):
                ax = self.subplots[self.cols * x + y]
                if ax is not None:
                    axes.append(ax)
                    ymin, ymax = ax.get_ylim(ymin, ymax)
            for ax in axes:
                ax.set_ylim(ymin, ymax)
            for ax in axes[1:]:
                ax.remove_ticks(xticks=False)

        for y in xrange(self.cols):
            xmin, xmax, axes = np.inf, -np.inf, []
            for x in xrange(self.rows):
                ax = self.subplots[self.cols * x + y]
                if ax is not None:
                    axes.append(ax)
                    xmin, xmax = ax.get_xlim(xmin, xmax)
            for ax in axes:
                ax.set_xlim(xmin, xmax)
            for ax in axes[0:-1]:
                ax.remove_ticks(yticks=False)

        self.fig.canvas.draw()
