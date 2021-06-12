#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test gazetteer aligment"""

import logging
from mygaz.aligment.pleiades import PleiadesAligner
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_PleiadesAligment(TestCase):

    def setUp(self):
        self.aligner = PleiadesAligner()

    def tearDown(self):
        """Change me"""
        pass

    def test_a(self):
        """Change me"""
        pass
