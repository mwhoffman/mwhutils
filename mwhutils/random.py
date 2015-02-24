"""
Random sampling.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from .random import rstate
from ._sobol import i4_sobol_generate

import numpy as np

__all__ = ['rstate']


def rstate(rng=None):
    """
    Return a numpy RandomState object. If an integer value is given then a new
    RandomState will be returned with this seed. If None is given then the
    global numpy state will be returned. If an already instantiated state is
    given this will be passed back.
    """
    if rng is None:
        return np.random.mtrand._rand
    elif isinstance(rng, np.random.RandomState):
        return rng
    elif isinstance(rng, int):
        return np.random.RandomState(rng)
    raise ValueError('unknown seed given to rstate')


