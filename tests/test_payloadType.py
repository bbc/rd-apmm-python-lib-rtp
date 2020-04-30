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
from rtp import PayloadType


class TestPayloadType (TestCase):
    def setUp(self):
        pass

    def test_isAudio(self):
        audioPT = set(range(0, 24))
        audioPT.add(33)

        for pt in audioPT:
            self.assertTrue(PayloadType(pt).isAudio())

        notAudioPT = set(range(0, 128)) - audioPT
        for pt in notAudioPT:
            self.assertFalse(PayloadType(pt).isAudio())

    def test_isVideo(self):
        videoPT = set(range(24, 35))

        for pt in videoPT:
            self.assertTrue(PayloadType(pt).isVideo())

        notVideoPT = set(range(0, 128)) - videoPT
        for pt in notVideoPT:
            self.assertFalse(PayloadType(pt).isVideo())

    def test_isAV(self):
        avPT = set([33])

        for pt in avPT:
            self.assertTrue(PayloadType(pt).isAV())

        notAVPT = set(range(0, 128)) - avPT
        for pt in notAVPT:
            self.assertFalse(PayloadType(pt).isAV())

    def test_isDynamic(self):
        dynPT = set(range(96, 128))

        for pt in dynPT:
            self.assertTrue(PayloadType(pt).isDynamic())

        notDynPT = set(range(0, 128)) - dynPT
        for pt in notDynPT:
            self.assertFalse(PayloadType(pt).isDynamic())

    def test_isUnassigned(self):
        unassignedPT = set(range(20, 25))
        unassignedPT.add(27)
        unassignedPT.update(set(range(29, 31)))
        unassignedPT.update(set(range(35, 72)))
        unassignedPT.update(set(range(77, 96)))

        for pt in unassignedPT:
            self.assertTrue(PayloadType(pt).isUnassigned())

        notUnassignedPT = set(range(0, 128)) - unassignedPT
        for pt in notUnassignedPT:
            self.assertFalse(PayloadType(pt).isUnassigned())

    def test_isReserved(self):
        reservedPT = set(range(1, 3))
        reservedPT.add(19)
        reservedPT.update(set(range(72, 77)))

        for pt in reservedPT:
            self.assertTrue(PayloadType(pt).isReserved())

        notReservedPT = set(range(0, 128)) - reservedPT
        for pt in notReservedPT:
            self.assertFalse(PayloadType(pt).isReserved())
