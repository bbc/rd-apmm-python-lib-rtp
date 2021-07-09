#!/usr/bin/python
#
# James Sandford, copyright BBC 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase
from hypothesis import given, example, strategies as st  # type: ignore

from rtp import RTP, PayloadType, Extension, CSRCList


class TestRTP (TestCase):
    def setUp(self):
        self.thisRTP = RTP()

    def setup_example(self):
        self.setUp()

    @given(
        st.booleans(),
        st.booleans(),
        st.sampled_from(PayloadType),
        st.integers(min_value=0, max_value=(2**16)-1),
        st.integers(min_value=0, max_value=(2**32)-1),
        st.integers(min_value=0, max_value=(2**32)-1),
        st.lists(st.integers(min_value=0, max_value=(2**16)-1), max_size=15),
        st.binary())
    def test_init(
       self,
       padding,
       marker,
       payloadType,
       sequenceNumber,
       timestamp,
       ssrc,
       csrcList,
       payload):
        newExt = Extension()
        newRTP = RTP(
            version=2,
            padding=padding,
            marker=marker,
            payloadType=payloadType,
            sequenceNumber=sequenceNumber,
            timestamp=timestamp,
            ssrc=ssrc,
            extension=newExt,
            csrcList=csrcList,
            payload=bytearray(payload))

        self.assertEqual(newRTP.version, 2)
        self.assertEqual(newRTP.padding, padding)
        self.assertEqual(newRTP.marker, marker)
        self.assertEqual(newRTP.payloadType, payloadType)
        self.assertEqual(newRTP.sequenceNumber, sequenceNumber)
        self.assertEqual(newRTP.timestamp, timestamp)
        self.assertEqual(newRTP.ssrc, ssrc)
        self.assertEqual(newRTP.extension, newExt)
        self.assertEqual(newRTP.csrcList, csrcList)
        self.assertEqual(newRTP.payload, payload)

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
        self.assertIsInstance(self.thisRTP.sequenceNumber, int)

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
        self.assertIsInstance(self.thisRTP.ssrc, int)

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
        self.assertEqual(self.thisRTP.payload, bytearray())

    @given(st.binary())
    def test_payload(self, value):
        self.thisRTP.payload = bytearray(value)
        self.assertEqual(self.thisRTP.payload, value)

    def test_payload_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisRTP.payload = ""

    def test_fromBytearray_default(self):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        default = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

        newRTP = RTP().fromBytearray(default)
        self.assertEqual(newRTP, self.thisRTP)

    def test_toBytearray_default(self):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.booleans())
    def test_fromBytearray_padding(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[0] |= value << 5
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.padding = value
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.booleans())
    def test_toBytearray_padding(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[0] |= value << 5
        self.thisRTP.padding = value
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.binary(min_size=2, max_size=2),
           st.binary(max_size=((2**16)-1)*4
                     ).filter(lambda x: (len(x) % 4) == 0))
    def test_fromBytearray_extension(self, startBits, headerExtension):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        newExt = Extension()
        newExt.startBits = bytearray(startBits)
        newExt.headerExtension = bytearray(headerExtension)

        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[0] |= 1 << 4
        payload[12:12] = newExt.toBytearray()
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.extension = newExt
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.binary(min_size=2, max_size=2),
           st.binary(max_size=((2**16)-1)*4
                     ).filter(lambda x: (len(x) % 4) == 0))
    def test_toBytearray_extension(self, startBits, headerExtension):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        newExt = Extension()
        newExt.startBits = bytearray(startBits)
        newExt.headerExtension = bytearray(headerExtension)

        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[0] |= 1 << 4
        expected[12:12] = newExt.toBytearray()
        self.thisRTP.extension = newExt
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_fromBytearray_csrcList(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[0] |= len(value)
        for x in range(len(value)):
            payload[12+(4*x):12+(4*x)] = value[x].to_bytes(4, byteorder='big')
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.csrcList.extend(value)
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.lists(st.integers(
        min_value=0, max_value=(2**16)-1), max_size=15))
    def test_toBytearray_csrcList(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[0] |= len(value)
        for x in range(len(value)):
            expected[12+(4*x):12+(4*x)] = value[x].to_bytes(4, byteorder='big')

        self.thisRTP.csrcList.extend(value)
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.booleans())
    def test_fromBytearray_marker(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[1] |= value << 7
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.marker = value
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.booleans())
    def test_toBytearray_marker(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[1] |= value << 7

        self.thisRTP.marker = value
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.sampled_from(PayloadType))
    def test_fromBytearray_payloadType(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[1] = value.value
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.payloadType = value
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.sampled_from(PayloadType))
    def test_toBytearray_payloadType(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[1] = value.value

        self.thisRTP.payloadType = value
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.integers(min_value=0, max_value=(2**16)-1))
    def test_fromBytearray_sequenceNumber(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[2:4] = value.to_bytes(2, byteorder='big')
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.sequenceNumber = value
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.integers(min_value=0, max_value=(2**16)-1))
    def test_toBytearray_sequenceNumber(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[2:4] = value.to_bytes(2, byteorder='big')
        self.thisRTP.sequenceNumber = value
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.integers(min_value=0, max_value=(2**32)-1))
    def test_fromBytearray_timestamp(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[4:8] = value.to_bytes(4, byteorder='big')
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.timestamp = value
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.integers(min_value=0, max_value=(2**32)-1))
    def test_toBytearray_timestamp(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[4:8] = value.to_bytes(4, byteorder='big')
        self.thisRTP.timestamp = value
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.integers(min_value=0, max_value=(2**32)-1))
    def test_fromBytearray_ssrc(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload[8:12] = value.to_bytes(4, byteorder='big')
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.ssrc = value
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.integers(min_value=0, max_value=(2**32)-1))
    def test_toBytearray_ssrc(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected[8:12] = value.to_bytes(4, byteorder='big')
        self.thisRTP.ssrc = value
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    @given(st.binary())
    def test_fromBytearray_payload(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        payload = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        payload += value
        newRTP = RTP().fromBytearray(payload)

        self.thisRTP.payload = bytearray(value)
        self.assertEqual(newRTP, self.thisRTP)

    @given(st.binary())
    def test_toBytearray_payload(self, value):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = bytearray(
            b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected += value
        self.thisRTP.payload = bytearray(value)
        self.assertEqual(self.thisRTP.toBytearray(), expected)

    def test_fromBytes_default(self):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        default = b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        newRTP = RTP().fromBytes(default)
        self.assertEqual(newRTP, self.thisRTP)

    def test_toBytes_default(self):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(self.thisRTP.toBytes(), expected)

    def test_bytes_default(self):
        self.thisRTP.sequenceNumber = 0
        self.thisRTP.ssrc = 0
        expected = b'\x80\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(bytes(self.thisRTP), expected)
