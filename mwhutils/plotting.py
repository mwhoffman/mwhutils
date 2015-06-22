"""
Plotting for various models.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import itertools as it
import matplotlib.pyplot as pl

__all__ = ['figure', 'plot_pairs', 'set_context', 'show']


def set_context(context):
    """
    Set the parameters for plotting according to the given context.
    """
    global PARAMS
    if context is 'screen':
        PARAMS = dict(
            colors=[
                (0.21568627450980393, 0.49411764705882355, 0.7215686274509804),
                (0.8941176470588236, 0.10196078431372549, 0.10980392156862745),
                (0.30196078431372547, 0.6862745098039216, 0.2901960784313726),
                (0.596078431372549, 0.3058823529411765, 0.6392156862745098),
                (1.0, 0.4980392156862745, 0.0),
                (0.6509803921568628, 0.33725490196078434, 0.1568627450980392),
                (0.9686274509803922, 0.5058823529411764, 0.7490196078431373)],
            dashes=[()],
            alphab=0.25,
            alpham=0.2,
            weight=2,
            markers=['o', 'x', 's', '+', 'D', '^'])
    elif context is 'paper':
        PARAMS = dict(
            colors=[
                (0.21568627450980393, 0.49411764705882355, 0.7215686274509804),
                (0.8941176470588236, 0.10196078431372549, 0.10980392156862745),
                (0.30196078431372547, 0.6862745098039216, 0.2901960784313726),
                (0.596078431372549, 0.3058823529411765, 0.6392156862745098),
                (1.0, 0.4980392156862745, 0.0),
                (0.6509803921568628, 0.33725490196078434, 0.1568627450980392),
                (0.9686274509803922, 0.5058823529411764, 0.7490196078431373)],
            dashes=[
                (),
                (8, 4),
                (6, 3, 2, 3),
                (2, 2),
                (6, 3, 2, 3, 2, 3),
                (4, 4)],
            alphab=0.25,
            alpham=0.2,
            weight=2,
            markers=['o', 'x', 's', '+', 'D', '^'])
    else:
        raise ValueError('unknown context')


# set the default context
set_context('screen')


class Axis(object):
    def __init__(self, ax, hook=None):
        self._ax = ax
        self._lim = (None, None, None, None)
        self._hook = (lambda: None) if (hook is None) else hook
        self._hold = False
        self._init()

    def _init(self):
        self._dashes = it.cycle(PARAMS['dashes'])
        self._markers = it.cycle(PARAMS['markers'])
        self._lcolors = it.cycle(PARAMS['colors'])
        self._mcolors = it.cycle(PARAMS['colors'])

        # pre-figure business
        self._ax.cla()
        self._ax.spines['top'].set_visible(False)
        self._ax.spines['right'].set_visible(False)
        self._ax.xaxis.set_tick_params(direction='out', top=False)
        self._ax.yaxis.set_tick_params(direction='out', right=False)
        self._ax.grid(color='k', ls='-', alpha=0.2, lw=0.5)

    # AXIS PROPERTIES =========================================================

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

    # UTILITY METHODS =========================================================

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

    # PLOTTING METHODS ========================================================

    def scatter(self, x, y, label=''):
        """
        Add a scatter plot to the axis.
        """
        marker = next(self._markers)
        self._ax.scatter(x, y, lw=1.5, marker=marker, color='k',
                         s=40, facecolors='none', label=label)
        self._draw()

    def scatterc(self, x, y, label=''):
        color = next(self._mcolors)
        self._ax.scatter(x, y, label=label, alpha=PARAMS['alpham'], color='k',
                         facecolor=color, lw=0.1)
        self._draw()

    def plot(self, x, y=None, lo=None, hi=None, add=True, label=''):
        """
        Add a simple plot to the axis.
        """
        if y is None:
            y = x
            x = np.arange(len(y))

        color = next(self._lcolors)
        dashes = next(self._dashes)
        self._ax.plot(x, y, ls='-', color=color, dashes=dashes, label=label,
                      lw=PARAMS['weight'])

        if (lo is not None) or (hi is not None):
            hi = ((y+hi) if add else hi) if (hi is not None) else (y+lo)
            lo = ((y-lo) if add else lo) if (lo is not None) else y
            self._ax.fill_between(x, lo, hi, color=color, 
                                  alpha=PARAMS['alphab'])

        self._draw()

    def vline(self, x, label=''):
        """
        Add a vertical line to the axis at x.
        """
        color = next(self._lcolors)
        self._ax.axvline(x, ls='--', lw=2, color=color, label=label)
        self._draw()

    def hline(self, y, label=''):
        """
        Add a horizontal line to the axis at y.
        """
        color = next(self._lcolors)
        self._ax.axhline(y, ls='--', lw=2, color=color, label=label)
        self._draw()

    def _draw(self):
        self._ax.axis('tight')
        self._ax.axis(self._lim)
        handles, labels = self._ax.get_legend_handles_labels()
        if len(handles) > 0:
            self._ax.legend(handles, labels, frameon=False, loc='best',
                            fontsize=12)
        self._hook()
        if not self._hold and pl.isinteractive():
            self.draw()

    def hold(self, hold=True):
        self._hold = hold

    def clear(self):
        self._init()
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


def figure(rows=1, cols=1, num=None, figsize=None):
    toolbar = pl.rcParams['toolbar']
    pl.rcParams['toolbar'] = 'None'
    fig = pl.figure(num, facecolor='white', figsize=figsize)
    fig.set_tight_layout(True)
    fig.clf()
    pl.rcParams['toolbar'] = toolbar

    if rows == cols == 1:
        return Axis(fig.gca())
    else:
        return Figure(fig, rows, cols)


def plot_pairs(samples, names=None, num=None):
    samples = np.array(samples, ndmin=2)
    _, d = samples.shape
    names = ['' for _ in xrange(d)] if (names is None) else names

    fig = figure(d-1, d-1, num=num)
    fig.hold()

    for i in xrange(d):
        for j in xrange(i+1, d):
            fig[j-1, i].scatterc(samples[:, i], samples[:, j])
            if i == 0:
                fig[j-1, i].ylabel = names[j]
            if j == d-1:
                fig[j-1, i].xlabel = names[i]

    fig.draw()
    return fig


def show():
    pl.show(not pl.isinteractive())
