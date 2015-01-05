"""
ABC tests.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from mwhutils.abc import ABCMeta, abstractmethod


def test_abc():
    """Test creation of an abstract base class."""

    class FooBase(object):
        """Base class."""
        __metaclass__ = ABCMeta

        @abstractmethod
        def method1(self):
            """Test."""
            pass

        def method2(self):
            """Test."""
            pass

    class Foo(FooBase):
        """Child class."""
        def method1(self):
            pass

        def method2(self):
            pass

    instance = Foo()
    assert instance.method1.__doc__ == "Test."
    assert instance.method2.__doc__ is None
