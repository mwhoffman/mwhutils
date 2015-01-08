"""
Modifications to ABC to allow for additional metaclass actions.
"""

# future imports
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

# global imports
from abc import ABCMeta as ABCMeta_
from abc import abstractmethod, abstractproperty

# exported symbols
__all__ = ['ABCMeta', 'abstractmethod', 'abstractproperty',
           'abstractclassmethod', 'abstractstaticmethod']


class ABCMeta(ABCMeta_):
    """
    Slight modification to ABCMeta that copies docstrings from an
    abstractmethod to its implementation if the implementation lacks a
    docstring.
    """
    def __new__(mcs, name, bases, attrs):
        # set up the new class.
        cls = super(ABCMeta, mcs).__new__(mcs, name, bases, attrs)

        # get all the methods that are abtract in one of our parents.
        abstracts = dict(
            (attr, getattr(base, attr))
            for base in bases
            for attr in getattr(base, '__abstractmethods__', set()))

        # loop through the methods that have an implementation in the class
        # that we just constructed.
        for attr in set(abstracts.keys()) - cls.__abstractmethods__:
            parent = abstracts[attr]
            child = getattr(cls, attr)
            docstring = getattr(parent, '__doc__', None)

            if docstring and not getattr(child, '__doc__', None):
                if isinstance(child, property):
                    setattr(cls, attr, property(child.fget, child.fset,
                                                child.fdel, docstring))
                elif hasattr(child, '__func__'):
                    child.__func__.__doc__ = docstring
                else:
                    child.__doc__ = docstring

        return cls


class abstractclassmethod(classmethod):
    """
    Decorator to create an abstract class method. This is a variation on the
    decorator introduced in Python 3. It has since been deprecated since
    classmethod can now be used to decorate an abstractmethod.
    """
    __isabstractmethod__ = True

    def __init__(self, function):
        function.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(function)


class abstractstaticmethod(staticmethod):
    """
    Decorator to create an abstract static method. This is a variation on the
    decorator introduced in Python 3. It has since been deprecated since
    staticmethod can now be used to decorate an abstractmethod.
    """
    __isabstractmethod__ = True

    def __init__(self, function):
        function.__isabstractmethod__ = True
        super(abstractstaticmethod, self).__init__(function)
