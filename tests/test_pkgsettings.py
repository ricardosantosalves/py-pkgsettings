#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pkgsettings
----------------------------------

Tests for `pkgsettings` module.
"""

import unittest

import pytest

from pkgsettings import DuplicateConfigureWarning, PrefixedSettings, Settings


class TestPkgsettings(unittest.TestCase):
    def setUp(self):
        super(TestPkgsettings, self).setUp()

    def test_default_settings(self):
        settings = Settings()
        settings.configure(debug=False)
        self.assertEqual(False, settings.debug)

    def test_context_manager(self):
        settings = Settings()
        settings.configure(debug=False)

        with settings(debug=True):
            self.assertEqual(True, settings.debug)
        self.assertEqual(False, settings.debug)

    def test_decorator(self):
        settings = Settings()
        settings.configure(debug=False)

        @settings(debug=True)
        def go():
            self.assertEqual(True, settings.debug)

        go()
        self.assertEqual(False, settings.debug)

    def test_decorator_in_class(self):
        _self = self
        settings = Settings()
        settings.configure(debug=False)

        class Dummy(object):
            @settings(debug=True)
            def go(self):
                _self.assertEqual(True, settings.debug)

        Dummy().go()
        self.assertEqual(False, settings.debug)

    def test_as_dict(self):
        settings = Settings()
        settings.configure(debug=False)

        with settings(debug=True):
            self.assertEqual(dict(debug=True), settings.as_dict())

        self.assertEqual(dict(debug=False), settings.as_dict())

    def test_with_object(self):
        class MySettings(object):
            def __init__(self):
                self.debug = False

        settings = Settings()
        settings.configure(MySettings())

        self.assertEqual(False, settings.debug)

        with settings(debug=True):
            self.assertEqual(True, settings.debug)

    def test_key_not_found(self):
        settings = Settings()
        settings.configure()

        with self.assertRaises(AttributeError):
            getattr(settings, "debug")

    def test_warning_when_adding_self(self):
        settings = Settings()
        settings.configure()

        with pytest.warns(DuplicateConfigureWarning):
            settings.configure(settings)

    def test_warning_when_adding_duplicate(self):
        settings = Settings()
        settings.configure()

        settings2 = Settings()
        settings2.configure(settings)

        with pytest.warns(DuplicateConfigureWarning):
            settings.configure(settings2)


class TestPrefixedSettings(unittest.TestCase):
    def test_no_prefix(self):
        ss = Settings()
        ss.configure(a=1, b="2")
        settings = PrefixedSettings(ss)
        self.assertEqual(1, settings.a)
        self.assertEqual("2", settings.b)

    def test_with_prefix(self):
        ss = Settings()
        ss.configure(MY_a=1, OTHER_a=2, a=3, c=5, MY_b="2")
        settings = PrefixedSettings(ss, "MY_")
        self.assertEqual(1, settings.a)
        self.assertEqual("2", settings.b)
        with self.assertRaises(AttributeError):
            a = settings.c
            self.fail(a)

        with self.assertRaises(AttributeError):
            a = settings.MY_a
            self.fail(a)


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
