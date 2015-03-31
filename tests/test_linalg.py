"""
Tests for linear algebra helpers.
"""

# pylint: disable=missing-docstring

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import numpy.testing as nt

import mwhutils.linalg as linalg


def test_add_diagonal():
    A = np.random.rand(5, 5)
    B = A.copy()
    C = linalg.add_diagonal(B, 1, copy=True)
    D = linalg.add_diagonal(B, 1, copy=False)

    nt.assert_equal(C, A + np.eye(5))
    nt.assert_equal(D, A + np.eye(5))
    assert C is not B
    assert D is B


def test_cholesky():
    A = np.random.rand(5, 5)
    A = linalg.add_diagonal(np.dot(A, A.T), 1)
    L = linalg.cholesky(A)
    nt.assert_allclose(np.dot(L, L.T), A)

    for order in ['C', 'F', 'A']:
        nt.assert_equal(L, linalg.cholesky(np.array(A, order=order)))

    A[0, 0] = -1
    nt.assert_raises(linalg.LinAlgError, linalg.cholesky, A)

    A = np.ones((10, 10))
    nt.assert_warns(UserWarning, linalg.cholesky, A)

    A = np.ones((10, 10)) - 0.5 * np.eye(10)
    nt.assert_raises(linalg.LinAlgError, linalg.cholesky, A)


def test_cholesky_update():
    A = np.random.rand(5, 5)
    A = linalg.add_diagonal(np.dot(A, A.T), 1)
    b = np.random.rand(5)

    L = linalg.cholesky(A)
    x = linalg.solve_triangular(L, b)

    L1 = linalg.cholesky(A[:3, :3])
    x1 = linalg.solve_triangular(L1, b[:3])

    L2 = linalg.cholesky_update(L1, A[3:, :3], A[3:, 3:])
    L2, x2 = linalg.cholesky_update(L1, A[3:, :3], A[3:, 3:], x1, b[3:])

    nt.assert_allclose(L, L2)
    nt.assert_allclose(x, x2)


def test_cholesky_inverse():
    A = np.random.rand(5, 5)
    A = linalg.add_diagonal(np.dot(A, A.T), 1)
    L = linalg.cholesky(A)
    invA1 = linalg.cholesky_inverse(L)
    invA2 = np.linalg.inv(A)
    nt.assert_allclose(invA1, invA2)

    for order in ['C', 'F', 'A']:
        invA2 = linalg.cholesky_inverse(np.array(L, order=order))
        nt.assert_equal(invA1, invA2)

    L = np.zeros((5, 5))
    L[:, 0] = 1
    nt.assert_raises(linalg.LinAlgError, linalg.cholesky_inverse, L)


def test_solve_triangular():
    A = np.random.rand(5, 5)
    A = linalg.add_diagonal(np.dot(A, A.T), 1)
    L = linalg.cholesky(A)
    B = np.random.rand(5, 2)

    X1 = linalg.solve_triangular(L, B)
    X2 = np.linalg.solve(L, B)
    nt.assert_allclose(X1, X2)

    for order1 in ['C', 'F', 'A']:
        for order2 in ['C', 'F', 'A']:
            X2 = linalg.solve_triangular(np.array(L, order=order1),
                                         np.array(B, order=order2))
            nt.assert_equal(X1, X2)

    X1 = linalg.solve_triangular(L, B, 1)
    X2 = np.linalg.solve(L.T, B)
    nt.assert_allclose(X1, X2)

    L = np.zeros((5, 5))
    L[:, 0] = 1
    nt.assert_raises(linalg.LinAlgError, linalg.solve_triangular, L, B)


def test_solve_cholesky():
    A = np.random.rand(5, 5)
    A = linalg.add_diagonal(np.dot(A, A.T), 1)
    L = linalg.cholesky(A)
    B = np.random.rand(5, 2)

    X1 = linalg.solve_cholesky(L, B)
    X2 = np.linalg.solve(A, B)
    nt.assert_allclose(X1, X2)

    for order1 in ['C', 'F', 'A']:
        for order2 in ['C', 'F', 'A']:
            X2 = linalg.solve_cholesky(np.array(L, order=order1),
                                       np.array(B, order=order2))
            nt.assert_equal(X1, X2)
