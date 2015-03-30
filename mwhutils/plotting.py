"""
Plotting for various models.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as pl

__all__ = ['figure']


class Axis(object):
    def __init__(self, ax, hold=False, hook=None):
        self._ax = ax
        self._lim = (None, None, None, None)
        self._hold = hold
        self._hook = (lambda: None) if (hook is None) else hook

        # pre-figure business
        self._ax.spines['top'].set_visible(False)
        self._ax.spines['right'].set_visible(False)

    def set_title(self, title):
        """
        Set the title of the axis.
        """
        self._ax.set_title(title)
        self._draw()

    def set_xlabel(self, xlabel):
        """
        Set the x-axis label.
        """
        self._ax.set_xlabel(xlabel)
        self._draw()

    def set_ylabel(self, ylabel):
        """
        Set the y-axis label.
        """
        self._ax.set_ylabel(ylabel)
        self._draw()

    def set_lim(self, xmin=None, xmax=None, ymin=None, ymax=None):
        """
        Set the limits of the axis.
        """
        self._lim = tuple(a if (b is None) else b
                          for (a, b) in
                          zip(self._lim, (xmin, xmax, ymin, ymax)))
        self._draw()

    def remove_ticks(self, xticks=True, yticks=True):
        """
        Remove the x/y ticks of the axis.
        """
        if xticks:
            self._ax.set_xticklabels([])
        if yticks:
            self._ax.set_yticklabels([])
        self._draw()

    def scatter(self, x, y):
        """
        Add a scatter plot to the axis.
        """
        self._ax.scatter(x, y, marker='o', s=30, lw=1, facecolors='none')
        self._draw()

    def plot(self, x, y):
        """
        Add a simple plot to the axis.
        """
        self._ax.plot(x, y)
        self._draw()

    def plot_banded(self, x, y, a=None, b=None):
        if a is None and b is None:
            lo = np.zeros_like(y)
            hi = y
        elif b is None:
            lo = y - a
            hi = y + a
        else:
            lo = y - a
            hi = y + b
        lines = self._ax.plot(x, y)
        color = lines[0].get_color()
        alpha = 0.25
        self._ax.fill_between(x, lo, hi, color=color, alpha=alpha)
        self._draw()

    def vline(self, x):
        """
        Add a vertical line to the axis at x.
        """
        self._ax.axvline(x, ls='--', color='r')
        self._draw()

    def hline(self, y):
        """
        Add a horizontal line to the axis at y.
        """
        self._ax.axhline(y, ls='--', color='r')
        self._draw()

    def _draw(self):
        self._ax.axis('tight')
        self._ax.axis(self._lim)
        self._hook()
        if (not self._hold) and pl.isinteractive():
            self.draw()

    def draw(self):
        self._ax.figure.canvas.draw()


class Figure(object):
    def __init__(self, fig=None, rows=1, cols=1, hold=False):
        self._fig = fig
        self._rows = rows
        self._cols = cols
        self._hold = hold
        self._axes = [None for _ in xrange(rows*cols)]

    def __getitem__(self, a):
        if self._rows == 1 or self._cols == 1:
            if not isinstance(a, int):
                raise ValueError('Figure must be indexed by an int')
        else:
            if not isinstance(a, tuple) or len(a) != 2:
                raise ValueError('Figure must be indexed by two ints')
            a = self._cols * a[0] + a[1]
        axis = self._axes[a]
        if axis is None:
            ax = self._fig.add_subplot(self._rows, self._cols, a+1)
            axis = Axis(ax, self._hold, self._hook)
            self._axes[a] = axis
        return axis

    def _hook(self):
        for x in xrange(self._rows):
            ymin = np.inf
            ymax = -np.inf
            axes = []
            for y in xrange(self._cols):
                axis = self._axes[self._cols * x + y]
                if axis is not None:
                    axes.append(axis._ax)
                    lims = axes[-1].axis()
                    ymin = min(ymin, lims[2])
                    ymax = max(ymax, lims[3])
            for ax in axes:
                ax.axis(ymin=ymin, ymax=ymax)
            for ax in axes[1:]:
                ax.set_yticklabels([])

        for y in xrange(self._cols):
            xmin = np.inf
            xmax = -np.inf
            axes = []
            for x in xrange(self._rows):
                axis = self._axes[self._cols * x + y]
                if axis is not None:
                    axes.append(axis._ax)
                    lims = axes[-1].axis()
                    xmin = min(xmin, lims[0])
                    xmax = max(xmax, lims[1])
            for ax in axes:
                ax.axis(xmin=xmin, xmax=xmax)
            for ax in axes[0:-1]:
                ax.set_xticklabels([])

    def draw(self):
        self._fig.canvas.draw()


def figure(fig=None, rows=1, cols=1, hold=False):
    if fig is None:
        fig = pl.figure()
    elif isinstance(fig, int):
        fig = pl.figure(fig)
    else:
        raise ValueError('figure identifier must be an integer')

    fig.clf()

    if rows == cols == 1:
        return Axis(fig.gca(), hold)
    else:
        return Figure(fig, rows, cols, hold)
