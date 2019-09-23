#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from unittest import TestCase

from rtp.rtp import RTP


class TestRTP (TestCase):
    def test_template(self):
        thisRTP = RTP()
        self.assertEqual(thisRTP.version, 2)
