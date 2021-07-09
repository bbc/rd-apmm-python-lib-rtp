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
from hypothesis import given, assume, strategies as st  # type: ignore

from rtp import Extension, LengthError


class TestExtension (TestCase):
    def setUp(self):
        self.thisExt = Extension()

    @given(st.binary(min_size=2, max_size=2),
           st.binary(max_size=((2**16)-1)*4
                     ).filter(lambda x: (len(x) % 4) == 0))
    def test_init(self, startBits, headerExtension):
        newExt = Extension(bytearray(startBits), bytearray(headerExtension))

        self.assertEqual(newExt.startBits, startBits)
        self.assertEqual(newExt.headerExtension, headerExtension)

    def test_startBits_default(self):
        self.assertEqual(self.thisExt.startBits, bytearray(2))

    @given(st.binary(min_size=2, max_size=2))
    def test_startBits(self, value):
        self.thisExt.startBits = bytearray(value)
        self.assertEqual(self.thisExt.startBits, value)

    def test_startBits_notBytes(self):
        with self.assertRaises(AttributeError):
            self.thisExt.startBits = ""

    @given(st.binary().filter(lambda x: len(x) != 2))
    def test_startBits_invalidSize(self, value):
        with self.assertRaises(LengthError):
            self.thisExt.startBits = bytearray(value)

    def test_headerExtension_default(self):
        self.assertEqual(self.thisExt.headerExtension, b'')

    @given(st.binary(max_size=((2**16)-1)*4))
    def test_headerExtension(self, value):
        if (len(value) % 4) == 0:
            self.thisExt.headerExtension = bytearray(value)
            self.assertEqual(self.thisExt.headerExtension, value)
        else:
            with self.assertRaises(LengthError):
                self.thisExt.headerExtension = bytearray(value)

    def test_headerExtension_tooLong(self):
        # This is the shortest value that's too long
        maxBytes = 4 * ((2**16) - 1)
        value = bytearray(maxBytes + 1)
        with self.assertRaises(LengthError):
            self.thisExt.headerExtension = bytearray(value)

        # The above value actually hits the check for 32-bit words.
        # So we'll test the shortest value thats too long and hits the 32-bit
        # word size too.
        value = bytearray(4 * (2**16))
        with self.assertRaises(LengthError):
            self.thisExt.headerExtension = bytearray(value)

    def test_headerExtension_notBytes(self):
        with self.assertRaises(AttributeError):
            self.thisExt.headerExtension = ""

    def test_bytearray_default(self):
        expected = bytearray(4)
        self.assertEqual(bytes(self.thisExt), expected)

        newExt = Extension().fromBytearray(expected)
        self.assertEqual(newExt, self.thisExt)

    @given(st.binary(min_size=2, max_size=2),
           st.binary(max_size=((2**16)-1)*4
                     ).filter(lambda x: (len(x) % 4) == 0))
    def test_toBytearray(self, startBits, headerExtension):
        self.thisExt.startBits = bytearray(startBits)
        self.thisExt.headerExtension = bytearray(headerExtension)

        thisExtB = self.thisExt.toBytearray()
        self.assertEqual(thisExtB[0:2], startBits)
        self.assertEqual(
            thisExtB[2:4],
            int(len(headerExtension)/4).to_bytes(2, byteorder='big'))
        self.assertEqual(thisExtB[4:], headerExtension)

    @given(st.binary(min_size=2, max_size=2),
           st.binary(max_size=((2**16)-1)*4
                     ).filter(lambda x: (len(x) % 4) == 0))
    def test_fromBytearray(self, startBits, headerExtension):
        bArray = bytearray(len(headerExtension) + 4)
        bArray[0:2] = startBits
        bArray[2:4] = int(len(headerExtension)/4).to_bytes(2, byteorder='big')
        bArray[4:] = headerExtension

        self.thisExt.fromBytearray(bArray)

        self.assertEqual(self.thisExt.startBits, startBits)
        self.assertEqual(self.thisExt.headerExtension, headerExtension)

        duplicateExt = Extension().fromBytearray(bArray)

        self.assertEqual(duplicateExt, self.thisExt)

    @given(st.binary(min_size=2, max_size=2),
           st.binary(max_size=((2**16)-1)*4
                     ).filter(lambda x: (len(x) % 4) == 0),
           st.integers(min_value=0, max_value=(2**16)-1))
    def test_fromBytearray_incorrectLen(
       self, startBits, headerExtension, length):
        assume(length != (len(headerExtension)/4))
        bArray = bytearray(len(headerExtension) + 4)
        bArray[0:2] = startBits
        bArray[2:4] = int(length).to_bytes(2, byteorder='big')
        bArray[4:] = headerExtension

        with self.assertRaises(LengthError):
            self.thisExt.fromBytearray(bArray)
