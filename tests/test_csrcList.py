#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from unittest import TestCase
from hypothesis import given, strategies as st

from rtp.rtp import CSRCList


class TestCSRCList (TestCase):
    def setUp(self):
        self.thisCSRCList = CSRCList()

    def setup_example(self):
        self.setUp()

    def test_csrc_default(self):
        self.assertEqual(self.thisCSRCList, [])

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_csrc_init(self, value):
        newCSRCList = CSRCList(value)
        self.assertEqual(newCSRCList, value)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), min_size=16))
    def test_csrc_init_too_big(self, value):
        with self.assertRaises(IndexError):
            CSRCList(value)

    @given(st.integers(min_value=0, max_value=(2**16)-1))
    def test_csrc_append(self, value):
        self.thisCSRCList.append(value)
        self.assertEqual(self.thisCSRCList, [value])

    def test_csrc_max_append(self):
        maxCSRCList = CSRCList([0]*15)
        self.assertEqual(len(maxCSRCList), 15)
        with self.assertRaises(IndexError):
            maxCSRCList.append(0)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_csrc_extend(self, value):
        self.thisCSRCList.extend(value)
        self.assertEqual(self.thisCSRCList, value)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_csrc_max_extend(self, value):
        maxCSRCList = CSRCList(value)
        appendLen = 16 - len(maxCSRCList)
        with self.assertRaises(IndexError):
            maxCSRCList.extend([0] * appendLen)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_csrc_iadd(self, value):
        self.thisCSRCList += value
        self.assertEqual(self.thisCSRCList, value)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_csrc_add(self, value):
        newCSRCList = self.thisCSRCList + value
        self.assertEqual(newCSRCList, value)
        self.assertEqual(self.thisCSRCList, [])

    @given(st.integers(min_value=0, max_value=14))
    def test_insert(self, index):
        baseList = [0]*15
        newCSRCList = CSRCList(baseList)
        newCSRCList.insert(index, 1)

        baseList.insert(index, 1)
        self.assertEqual(newCSRCList, baseList)

    def test_insert_invalid(self):
        baseList = [0]*15
        newCSRCList = CSRCList(baseList)

        with self.assertRaises(IndexError):
            newCSRCList.insert(-1, 1)

        with self.assertRaises(IndexError):
            newCSRCList.insert(len(baseList), 1)

    @given(st.integers(min_value=0, max_value=(2**32) - 1))
    def test_csrcIsValid(self, value):
        self.thisCSRCList.csrcIsValid(value)

    def test_csrcIsValid_invalid(self):
        with self.assertRaises(AttributeError):
            self.thisCSRCList.csrcIsValid("")

        with self.assertRaises(ValueError):
            self.thisCSRCList.csrcIsValid(2**32)

    @given(st.integers(max_value=-1))
    def test_csrcIsValid_tooSmall(self, value):
        with self.assertRaises(ValueError):
            self.thisCSRCList.csrcIsValid(value)
