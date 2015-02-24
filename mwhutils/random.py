"""
Random sampling.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np

__all__ = ['rstate', 'wishart']


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


def wishart(Sigma, dof, rng=None):
    """
    Return a sample from the Wishart distribution with scale matrix `Sigma` and
    `dof` degrees of freedom.
    """
    rng = rstate(rng)
    d = Sigma.shape[0]
    L = np.linalg.cholesky(Sigma)

    if (dof <= 81+d) and (dof == round(dof)):
        # for small enough dof just use the standard definition
        X = np.dot(L, rng.normal(size=(d, dof)))

    else:
        # otherwise use the procedure of Smith & Hocking, where the cholesky is
        # multiplied by A which has sqrt of chi-square variables on its
        # diagonal and standard normal elements on the upper triangle.
        A = np.diag(np.sqrt(rng.chisquare(dof - np.arange(0, d), size=d)))
        A[np.tri(d, k=-1, dtype=bool)] = rng.normal(size=(d*(d-1)/2.))
        X = np.dot(L, A)

    return np.dot(X, X.T)
