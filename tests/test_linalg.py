"""
Linalg tests.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import scipy.linalg as sla
import numpy.testing as nt

from mwhutils.linalg import chol_update


def test_chol_update():
    """Test the incremental cholesky decomposition."""
    A = np.random.rand(5, 5)
    A = np.dot(A.T, A)
    b = np.random.rand(5, 2)

    R1 = sla.cholesky(A[:3, :3])
    x1 = sla.solve_triangular(R1, b[:3], trans=True)
    R1, x1 = chol_update(R1, A[:3, 3:], A[3:, 3:], x1, b[3:])

    R2 = sla.cholesky(A)
    x2 = sla.solve_triangular(R2, b, trans=True)

    nt.assert_allclose(x1, x2)
