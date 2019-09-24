#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from unittest import TestCase
from hypothesis import given, strategies as st

from rtp.rtp import Extension


class TestExtension (TestCase):
    def setUp(self):
        self.thisExt = Extension()

    def test_startBits_default(self):
        self.assertEqual(self.thisExt.startBits, b'\x00\x00')

    @given(st.binary(min_size=2, max_size=2))
    def test_startBits(self, value):
        self.thisExt.startBits = value
        self.assertEqual(self.thisExt.startBits, value)

    def test_startBits_notBytes(self):
        with self.assertRaises(AttributeError):
            self.thisExt.startBits = ""

    @given(st.binary().filter(lambda x: len(x) != 2))
    def test_startBits_invalidSize(self, value):
        with self.assertRaises(ValueError):
            self.thisExt.startBits = value

    def test_headerExtension_default(self):
        self.assertEqual(self.thisExt.headerExtension, b'')

    @given(st.binary(max_size=((2**16)-1)*4))
    def test_headerExtension(self, value):
        if (len(value) % 4) == 0:
            self.thisExt.headerExtension = value
            self.assertEqual(self.thisExt.headerExtension, value)
        else:
            with self.assertRaises(ValueError):
                self.thisExt.headerExtension = value

    def test_headerExtension_tooLong(self):
        # This is the shortest value that's too long
        value = b'\x00\x00\x00\x00' * ((2**16) - 1)
        value += b'\x00'
        with self.assertRaises(ValueError):
            self.thisExt.headerExtension = value

        # The above value actually hits the check for 32-bit words.
        # So we'll test the shortest value thats too long and hits the 32-bit
        # word size too.
        value = b'\x00\x00\x00\x00' * (2**16)
        with self.assertRaises(ValueError):
            self.thisExt.headerExtension = value

    def test_headerExtension_notBytes(self):
        with self.assertRaises(AttributeError):
            self.thisExt.headerExtension = ""
