"""
ABC tests.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy.testing as nt
import mwhutils.abc as abc


def test_abc():
    """Test creation of an abstract base class."""

    class FooBase(object):
        """Base class."""

        __metaclass__ = abc.ABCMeta

        def method(self):
            """Method"""

        @abc.abstractmethod
        def abstract_method1(self):
            """Method 1"""

        @abc.abstractmethod
        def abstract_method2(self):
            """Method 2"""

        @abc.abstractclassmethod
        def abstract_classmethod(cls):
            """Class method"""

        @abc.abstractstaticmethod
        def abstract_staticmethod():
            """Static method"""

        @abc.abstractproperty
        def abstract_property(self):
            """Property"""

    class Foo(FooBase):
        """Child class."""

        def method(self):
            """New method"""
            pass

        def abstract_method1(self):
            return 1

        def abstract_method2(self):
            """Method 3"""
            return 2

        @classmethod
        def abstract_classmethod(cls):
            return 3

        @staticmethod
        def abstract_staticmethod():
            return 4

        @property
        def abstract_property(self):
            return 5

    # Make sure the abstract class can't be instantiated
    nt.assert_raises(TypeError, FooBase)

    # check the docstrings
    assert Foo.method.__doc__ == "New method"
    assert Foo.abstract_method1.__doc__ == "Method 1"
    assert Foo.abstract_method2.__doc__ == "Method 3"
    assert Foo.abstract_classmethod.__doc__ == "Class method"
    assert Foo.abstract_staticmethod.__doc__ == "Static method"
    assert Foo.abstract_property.__doc__ == "Property"

    # Make sure the instance can be instantiated
    foo = Foo()

    # check the implementations
    assert foo.abstract_method1() == 1
    assert foo.abstract_method2() == 2
    assert foo.abstract_classmethod() == 3
    assert foo.abstract_staticmethod() == 4
    assert foo.abstract_property == 5
