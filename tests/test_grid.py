"""
Random and quasi-random generator tests.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy.testing as nt

from mwhutils.random import rstate
from mwhutils.grid import uniform, latin, sobol, regular


def test_rstate():
    """Test the rstate helper."""
    rng = rstate()
    rng = rstate(rng)
    rng1 = rstate(1)
    rng2 = rstate(1)

    nt.assert_equal(rng1.randint(5), rng2.randint(5))
    nt.assert_raises(ValueError, rstate, 'foo')


def check_random(method):
    """Check that the method implements the random-generator interface."""
    bounds = [(0, 1), (3, 4)]
    sample = method(bounds, 10)
    assert sample.shape == (10, 2)
    assert all(sample[:, 0] >= 0) and all(sample[:, 0] <= 1)
    assert all(sample[:, 1] >= 3) and all(sample[:, 1] <= 4)

    sample = regular((0, 1), 10)
    assert sample.shape == (10, 1)
    assert all(sample[:, 0] >= 0) and all(sample[:, 0] <= 1)


def test_random():
    """Test all the random generators."""
    for method in [uniform, latin, sobol]:
        yield check_random, method


def test_regular():
    """Test the non-random regular "sampler"."""
    sample = regular([(0, 1), (3, 4)], 10)
    assert sample.shape == (100, 2)
    assert all(sample[:, 0] >= 0) and all(sample[:, 0] <= 1)
    assert all(sample[:, 1] >= 3) and all(sample[:, 1] <= 4)

    sample = regular((0, 1), 10)
    assert sample.shape == (10, 1)
    assert all(sample[:, 0] >= 0) and all(sample[:, 0] <= 1)
