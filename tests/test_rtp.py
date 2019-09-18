#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from __future__ import print_function
from __future__ import absolute_import
from unittest import TestCase

from rtp import template


class Testrtp (TestCase):
    def test_template(self):
        self.assertTrue(template)
