#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from unittest import TestCase
from hypothesis import given, example, strategies as st

from rtp.rtp import RTP, PayloadType, Extension, CSRCList


class TestRTP (TestCase):
    def setUp(self):
        self.thisRTP = RTP()

    def test_version_default(self):
        # Test default
        self.assertEqual(self.thisRTP.version, 2)

    @given(st.integers())
    @example(2)
    def test_version(self, value):
        if value == 2:
            self.thisRTP.version = value
            self.assertEqual(self.thisRTP.version, value)
        else:
            with self.assertRaises(ValueError):
                self.thisRTP.version = value

    def test_padding_default(self):
        self.assertEqual(self.thisRTP.padding, False)

    @given(st.booleans())
    def test_padding(self, value):
        self.thisRTP.padding = value
        self.assertEqual(self.thisRTP.padding, value)

    def test_padding_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.padding = ""

    def test_marker_default(self):
        self.assertEqual(self.thisRTP.marker, False)

    @given(st.booleans())
    def test_marker(self, value):
        self.thisRTP.marker = value
        self.assertEqual(self.thisRTP.marker, value)

    def test_marker_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.marker = ""

    def test_payloadType_default(self):
        self.assertEqual(self.thisRTP.payloadType, PayloadType.DYNAMIC_96)

    @given(st.sampled_from(PayloadType))
    def test_payloadType(self, value):
        self.thisRTP.payloadType = value
        self.assertEqual(self.thisRTP.payloadType, value)

    def test_payloadType_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.payloadType = ""

    def test_sequenceNumber_default(self):
        self.assertEqual(self.thisRTP.sequenceNumber, 0)

    @given(st.integers(min_value=0, max_value=(2**16)-1))
    def test_sequenceNumber_valid(self, value):
        self.thisRTP.sequenceNumber = value
        self.assertEqual(self.thisRTP.sequenceNumber, value)

    @given(st.integers().filter(lambda x: (x < 0) or (x >= 2**16)))
    def test_sequenceNumber_invalid(self, value):
        with self.assertRaises(ValueError):
            self.thisRTP.sequenceNumber = value

    def test_sequenceNumber_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.sequenceNumber = ""

    def test_timestamp_default(self):
        self.assertEqual(self.thisRTP.timestamp, 0)

    @given(st.integers(min_value=0, max_value=(2**32)-1))
    def test_timestamp_valid(self, value):
        self.thisRTP.timestamp = value
        self.assertEqual(self.thisRTP.timestamp, value)

    @given(st.integers().filter(lambda x: (x < 0) or (x >= 2**32)))
    def test_timestamp_invalid(self, value):
        with self.assertRaises(ValueError):
            self.thisRTP.timestamp = value

    def test_timestamp_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.timestamp = ""

    def test_ssrc_default(self):
        self.assertEqual(self.thisRTP.ssrc, 0)

    @given(st.integers(min_value=0, max_value=(2**32)-1))
    def test_ssrc_valid(self, value):
        self.thisRTP.ssrc = value
        self.assertEqual(self.thisRTP.ssrc, value)

    @given(st.integers().filter(lambda x: (x < 0) or (x >= 2**32)))
    def test_ssrc_invalid(self, value):
        with self.assertRaises(ValueError):
            self.thisRTP.ssrc = value

    def test_ssrc_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.ssrc = ""

    def test_extension_default(self):
        self.assertEqual(self.thisRTP.extension, None)

    def test_extension(self):
        self.thisRTP.extension = None
        self.assertEqual(self.thisRTP.extension, None)

        newExt = Extension()
        self.thisRTP.extension = newExt
        self.assertEqual(self.thisRTP.extension, newExt)

    def test_extension_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.extension = ""

    def test_csrcList_default(self):
        self.assertEqual(self.thisRTP.csrcList, CSRCList())

    def test_payload_default(self):
        self.assertEqual(self.thisRTP.payload, b'')

    @given(st.binary())
    def test_payload(self, value):
        self.thisRTP.payload = value
        self.assertEqual(self.thisRTP.payload, value)

    def test_payload_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.payload = ""
