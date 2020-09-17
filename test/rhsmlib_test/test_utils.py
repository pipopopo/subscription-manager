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
Unit tests for module rhsmlib.utils.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest


from rhsmlib.utils import Singleton, no_reinitialization


class Child(Singleton):
    """
    Class used for testing of Singleton subclass
    """
    @no_reinitialization
    def __init__(self, foo=None, bar=None):
        self.foo = foo
        self.bar = bar


class GrandSon(Child):
    """
    Another class used for testing of Singleton subclass.
    In this subclass is re-initialization of Singleton forbidden
    using decorator @no_reinitialization
    """
    @no_reinitialization
    def __init__(self, foo=None, bar=None):
        super(GrandSon, self).__init__(foo=foo, bar=bar)


class GrandDaughter(Child):
    """
    Another class used for testing of Singleton subclass.
    Note that Child uses no_reinitialization and this
    class doesn't.
    """
    def __init__(self, foo=None, bar=None):
        super(GrandDaughter, self).__init__(foo=foo, bar=bar)


class Kid(Singleton):
    """
    Another class used for testing of Singleton subclass. Calling
    GrandDaughter() with new arguments will cause re-initialization
    of singleton. Note that Child uses no_reinitialization and this
    class doesn't
    """
    def __init__(self, foo=None, bar=None):
        self.foo = foo
        self.bar = bar


class SingletonTestCase(unittest.TestCase):

    def setUp(self):
        """
        This method all singleton instances before each test
        """
        Singleton._instance = None
        Child._instance = None
        GrandSon._instance = None
        GrandDaughter._instance = None
        Kid._instance = None

    def test_is_singleton(self):
        """
        Simple test of singleton
        """
        s1 = Singleton()
        s2 = Singleton()
        self.assertEqual(id(s1), id(s2))

    def test_is_subclass_singleton(self):
        """
        Test of singleton and child of singleton

        """
        s = Singleton()
        ch1 = Child()
        ch2 = Child()
        self.assertNotEqual(id(s), id(ch1))
        self.assertEqual(id(ch1), id(ch2))

    def test_child_is_initialized(self):
        """
        Test that instance of class is initialized
        """
        ch = Child("foo", bar="bar")
        self.assertEqual(ch.bar, "bar")
        self.assertEqual(ch.foo, "foo")

    def test_another_child_is_not_reinitialized(self):
        """
        Test of decorator no_reinitialization
        """
        ch1 = Child("foo", bar="bar")
        self.assertEqual(ch1.bar, "bar")
        self.assertEqual(ch1.foo, "foo")
        ch2 = Child("FOO", bar="BAR")
        # This singleton should still have still old values
        self.assertEqual(ch2.bar, "bar")
        self.assertEqual(ch2.foo, "foo")

    def test_grand_son(self):
        """
        Test of decorator no_reinitialization (subclass of child)
        """
        ch1 = Child("foo", bar="bar")
        ch2 = Child("foolish", bar="barista")
        gs = GrandSon("FOO", bar="BAR")
        self.assertNotEqual(id(ch1), id(gs))
        self.assertEqual(ch1.foo, "foo")
        self.assertEqual(ch2.bar, "bar")
        self.assertEqual(gs.foo, "FOO")
        self.assertEqual(gs.bar, "BAR")

    def test_grand_daughter(self):
        """
        This test is intended for testing class without decorator no_reinitialization
        """
        # Create instance of singleton with some arguments
        gd1 = GrandDaughter("foo", bar="bar")
        self.assertEqual(gd1.foo, "foo")
        self.assertEqual(gd1.bar, "bar")
        # No try to get instance with some different arguments
        gd2 = GrandDaughter("FOO", bar="BAR")
        self.assertEqual(id(gd1), id(gd2))
        # This singleton should have new values
        self.assertEqual(gd2.foo, "foo")
        self.assertEqual(gd2.bar, "bar")

    def test_kid(self):
        """
        This test is intended for testing class without decorator no_reinitialization. Parent
        of this class does not use the decorator no_reinitialization
        """
        # Create instance of singleton with some arguments
        kid1 = Kid("foo", bar="bar")
        self.assertEqual(kid1.foo, "foo")
        self.assertEqual(kid1.bar, "bar")
        # No try to get instance with some different arguments
        kid2 = Kid("FOO", bar="BAR")
        self.assertEqual(id(kid1), id(kid2))
        # This singleton should have new values
        self.assertEqual(kid2.foo, "FOO")
        self.assertEqual(kid2.bar, "BAR")
