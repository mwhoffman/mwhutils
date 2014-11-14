"""
Linear algebra helper functions.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import scipy.linalg as sla

__all__ = ['chol_update']


def chol_update(A, B, C, a, b):
    """
    Update the cholesky decomposition of a growing matrix.

    Let `A` denote a cholesky decomposition of some matrix and `a` the inverse
    of `A` applied to some vector `y`. This computes the cholesky to a new
    matrix which has additional elements `B` and the non-diagonal and `C` on
    the diagonal block. It also computes the solution to the application of the
    inverse where the vector has additional elements `b`.
    """
    n = A.shape[0]
    m = C.shape[0]

    B = sla.solve_triangular(A, B, trans=True)
    C = sla.cholesky(C - np.dot(B.T, B))
    c = np.dot(B.T, a)

    # grow the new cholesky and use then use this to grow the vector a.
    A = np.r_[np.c_[A, B], np.c_[np.zeros((m, n)), C]]
    a = np.r_[a, sla.solve_triangular(C, b-c, trans=True)]

    return A, a
