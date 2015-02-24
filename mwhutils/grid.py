"""
Generate samples from a (random) grid. This includes uniform samples, an actual
grid, and low-discrepancy sequences.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from .random import rstate
from ._sobol import i4_sobol_generate

import numpy as np

__all__ = ['uniform', 'latin', 'sobol', 'regular']


def uniform(bounds, n, rng=None):
    """
    Sample n points uniformly at random from the specified region, given by
    a list of [(lo,hi), ..] bounds in each dimension.
    """
    # if given a seed or an instantiated RandomState make sure that we use
    # it here, but also within the sample_spectrum code.
    rng = rstate(rng)
    bounds = np.array(bounds, ndmin=2, copy=False)

    # generate the random values.
    d = len(bounds)
    w = bounds[:, 1] - bounds[:, 0]
    X = bounds[:, 0] + w * rng.rand(n, d)

    return X


def latin(bounds, n, rng=None):
    """
    Sample n points from a latin hypercube within the specified region, given
    by a list of [(lo,hi), ..] bounds in each dimension.
    """
    rng = rstate(rng)
    bounds = np.array(bounds, ndmin=2, copy=False)

    # generate the random samples.
    d = len(bounds)
    w = bounds[:, 1] - bounds[:, 0]
    X = bounds[:, 0] + w * (np.arange(n)[:, None] + rng.rand(n, d)) / n

    # shuffle each dimension.
    for i in xrange(d):
        X[:, i] = rng.permutation(X[:, i])

    return X


def sobol(bounds, n, rng=None):
    """
    Sample n points from a sobol sequence within the specified region, given by
    a list of [(lo,hi), ..] bounds in each dimension.
    """
    rng = rstate(rng)
    bounds = np.array(bounds, ndmin=2, copy=False)

    # generate the random samples.
    d = len(bounds)
    skip = rng.randint(100, 200)
    w = bounds[:, 1] - bounds[:, 0]
    X = bounds[:, 0] + w * i4_sobol_generate(d, n, skip).T

    return X


def regular(bounds, n):
    """
    Generate a regular grid within the specified region, given by `bounds`,
    a list of [(lo,hi), ..] bounds in each dimension. `n` represents the number
    of points along each dimension.
    """
    bounds = np.array(bounds, ndmin=2, copy=False)
    d = len(bounds)

    if d == 1:
        X = np.linspace(bounds[0, 0], bounds[0, 1], n)
        X = np.reshape(X, (-1, 1))
    else:
        X = np.meshgrid(*(np.linspace(a, b, n) for a, b in bounds))
        X = np.reshape(X, (d, -1)).T

    return X
