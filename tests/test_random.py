"""
Random sampler tests.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import numpy.testing as nt
import mwhutils.random as random


def test_rstate():
    """Test the rstate helper."""
    rng = random.rstate()
    rng = random.rstate(rng)
    rng1 = random.rstate(1)
    rng2 = random.rstate(1)

    nt.assert_equal(rng1.randint(5), rng2.randint(5))
    nt.assert_raises(ValueError, random.rstate, 'foo')


def test_wishart():
    Sigma1 = random.wishart(np.eye(5), 5)
    Sigma2 = random.wishart(Sigma1, 5)
    Sigma3 = random.wishart(Sigma1, 120)

    np.linalg.cholesky(Sigma1)
    np.linalg.cholesky(Sigma2)
    np.linalg.cholesky(Sigma3)
