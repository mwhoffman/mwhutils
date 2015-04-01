"""
Tests for plotting.
"""

# pylint: disable=missing-docstring

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as pl
import numpy as np
import numpy.testing as nt

import mwhutils.plotting as mp


def test_single():
    x = np.linspace(0, 2*np.pi, 500)
    pl.ion()
    fig = mp.figure(1)
    fig.plot(x, x)
    fig.plot_banded(x, x)
    fig.plot_banded(x, x, 1)
    fig.plot_banded(x, x, 1, 2)
    fig.scatter(x, x)
    fig.hline(0.5)
    fig.vline(0.5)
    fig.set_title('foo')
    fig.set_xlabel('bar')
    fig.set_ylabel('baz')
    fig.set_lim(0, 1, 0, 1)
    fig.hold()
    fig.remove_ticks(False, False)
    fig.remove_ticks()
    fig.draw()
    mp.show()
    fig.clear()


def test_grid():
    x = np.linspace(0, 2*np.pi, 500)
    fig = mp.figure(rows=2)
    nt.assert_raises(ValueError, fig.__getitem__, 'a')
    fig[0].plot(x, np.sin(x))

    fig = mp.figure(rows=2, cols=2)
    nt.assert_raises(ValueError, fig.__getitem__, 'a')

    fig.hold()
    fig[0, 0].plot(x, np.sin(x))
    fig[0, 1].plot(x, np.sin(x))
    fig[1, 0].plot(x, np.sin(x))
    fig[1, 1].plot(x, np.sin(x))
    fig.draw()
    fig.clear()


def test_plot_pairs():
    A = np.random.rand(100, 5)
    mp.plot_pairs(A)
    mp.plot_pairs(A, map(str, range(5)))
