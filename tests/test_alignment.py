#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test gazetteer aligment"""

from datetime import datetime, timedelta
import logging
from mygaz.aligment.pleiades import PleiadesAligner
from nose.tools import assert_equal, assert_false, assert_true, raises
import os
from pathlib import Path
from time import mktime
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_PleiadesAlignment_Init(TestCase):
    def test_init_names_index(self):
        cache_path = Path(
            '/'.join(
                (__file__, '../../data/cache/name_index.json'))).resolve()
        os.remove(cache_path)
        aligner = PleiadesAligner()
        aligner._fetch_names_index(cache_override=True)
        aligner._fetch_names_index(cache_override=False)
        now = datetime.today()
        ereyesterday = now - 2 * aligner.cache_duration
        when = mktime(ereyesterday.timetuple())
        os.utime(cache_path, times=(when, when))
        aligner._fetch_names_index()
        del aligner


class Test_PleiadesAlignment(TestCase):

    def setUp(self):
        self.aligner = PleiadesAligner()

    def tearDown(self):
        """Change me"""
        del self.aligner

