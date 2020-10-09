from __future__ import print_function, division, absolute_import

# Copyright (c) 2017 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

"""
This module includes several utils that could be used by several client
applications.
"""


import threading


def no_reinitialization(init_method):
    """
    Decorator of singleton __init__ method. When the __init__ method will be wrapped using
    this decorator, then the __init__ method will be called only once, when the first instance
    is created.
    :param init_method: the __init__ method of singleton object
    :return: wrapper function
    """

    def wrapper(*args, **kwargs):
        if len(args) > 0:
            self = args[0]

            # Using this wrapper with something else will cause exception
            assert hasattr(self, "_initialized") is True, \
                "The {cls} does not include _initialized attribute".format(cls=self.__class__)
            assert hasattr(self, '_lock') is True, \
                "The {cls} does not include _lock attribute".format(cls=self.__class__)

            # When we know that the object contains _lock, then we can lock it
            self._lock.acquire(blocking=True)

            # Encapsulate init method in try-finally statement, because anything can
            # happen in the init_method
            try:
                if self._initialized is True:
                    return
                init_method(*args, **kwargs)
            finally:
                self._initialized = True
                self._lock.release()
        else:
            raise AssertionError("The wrapper method was called without any argument")

    return wrapper


class Singleton(object):
    """
    Singleton and parent for singletons. Please use decorator for __init__ method like this:

    class Child(Singleton):
        @no_reinitialization
        def __init__(self, foo, bar=None):
            self.foo = foo
            self.bar = bar

    The behavior of singleton without using @no_reinitialization is usually not desired,
    because __init__() would re-initialize instance of singleton everytime it is called.
    """
    _instance = None
    _initialized = False

    _lock = None

    def __new__(cls, *args, **kwargs):
        """
        Function called, when new instance of Singleton is requested
        """
        if cls._lock is None:
            cls._lock = threading.RLock()

        cls._lock.acquire(blocking=True)
        if not isinstance(cls._instance, cls):
            # When there is not existing instance, then create first one
            cls._instance = object.__new__(cls)
        cls._lock.release()

        return cls._instance
