"""
Plotting for various models.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as pl

__all__ = ['figure', 'plot_pairs', 'show']


class Axis(object):
    def __init__(self, ax, hook=None):
        self._ax = ax
        self._lim = (None, None, None, None)
        self._hook = (lambda: None) if (hook is None) else hook
        self._hold = False

        # pre-figure business
        self._ax.spines['top'].set_visible(False)
        self._ax.spines['right'].set_visible(False)
        self._ax.get_xaxis().tick_bottom()
        self._ax.get_yaxis().tick_left()

    ### AXIS PROPERTIES =======================================================

    @property
    def title(self):
        """Get/set the title of the axis."""
        return self._ax.get_title()

    @property
    def xlabel(self):
        """Get/set the x-axis label."""
        self._ax.get_xlabel()

    @property
    def ylabel(self):
        """Get/set the y-axis label."""
        self._ax.get_ylabel()

    @title.setter
    def title(self, title):
        self._ax.set_title(title)
        self._draw()

    @xlabel.setter
    def xlabel(self, xlabel):
        self._ax.set_xlabel(xlabel)
        self._draw()

    @ylabel.setter
    def ylabel(self, ylabel):
        self._ax.set_ylabel(ylabel)
        self._draw()

    ### UTILITY METHODS =======================================================

    def set_lim(self, xmin=None, xmax=None, ymin=None, ymax=None):
        """
        Set the limits of the axis.
        """
        self._lim = (xmin, xmax, ymin, ymax)
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

    ### PLOTTING METHODS ======================================================

    def scatter(self, x, y, marker='o', color='k', alpha=1):
        """
        Add a scatter plot to the axis.
        """
        kwargs = dict(lw=1.5, marker=marker, color=color, alpha=alpha)
        if marker is 'o':
            kwargs['s'] = 30
            kwargs['facecolors'] = 'none'
        else:
            kwargs['s'] = 40

        self._ax.scatter(x, y, **kwargs)
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
        if not self._hold and pl.isinteractive():
            self.draw()

    def hold(self, hold=True):
        self._hold = hold

    def clear(self):
        self._ax.cla()
        self._draw()

    def draw(self):
        self._hold = False
        self._ax.figure.canvas.draw()
        self._ax.figure.show(warn=False)


class Figure(object):
    def __init__(self, fig, rows, cols):
        self._fig = fig
        self._rows = rows
        self._cols = cols
        self._axes = [None for _ in xrange(rows*cols)]
        self._hold = False

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
            axis = Axis(ax, self._hook)
            self._axes[a] = axis
        axis.hold(axis._hold or self._hold)
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

    def hold(self, hold=True):
        self._hold = hold

    def clear(self):
        self._fig.clf()
        self._axes = [None for _ in self._axes]

    def draw(self):
        self._hold = False
        for axis in self._axes:
            if axis is not None:
                axis.hold(False)
        self._fig.canvas.draw()
        self._fig.show(warn=False)


def figure(num=None, rows=1, cols=1):
    toolbar = pl.rcParams['toolbar']
    pl.rcParams['toolbar'] = 'None'
    fig = pl.figure(num, facecolor='white')
    fig.set_tight_layout(True)
    fig.clf()
    pl.rcParams['toolbar'] = toolbar

    if rows == cols == 1:
        return Axis(fig.gca())
    else:
        return Figure(fig, rows, cols)


def plot_pairs(samples, names=None, fig=None):
    samples = np.array(samples, ndmin=2)
    _, d = samples.shape
    names = ['' for _ in xrange(d)] if (names is None) else names

    fig = figure(fig, d-1, d-1)
    fig.hold()

    for i in xrange(d):
        for j in xrange(i+1, d):
            fig[j-1, i].scatter(samples[:, i], samples[:, j], alpha=0.1)
            if i == 0:
                fig[j-1, i].ylabel = names[j]
            if j == d-1:
                fig[j-1, i].xlabel = names[i]

    fig.draw()
    return fig


def show():
    pl.show(not pl.isinteractive())
