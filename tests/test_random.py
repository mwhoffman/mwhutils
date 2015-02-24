"""
Random sampler tests.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy.testing as nt

from mwhutils.random import rstate


def test_rstate():
    """Test the rstate helper."""
    rng = rstate()
    rng = rstate(rng)
    rng1 = rstate(1)
    rng2 = rstate(1)

    nt.assert_equal(rng1.randint(5), rng2.randint(5))
    nt.assert_raises(ValueError, rstate, 'foo')

