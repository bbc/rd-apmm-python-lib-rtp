#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

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
