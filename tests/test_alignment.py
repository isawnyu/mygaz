#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test gazetteer aligment"""

from datetime import datetime, timedelta
import json
import logging
from mygaz.alignment.aligner import Aligner
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


class Test_Aligner_Init(TestCase):
    def test_init(self):
        cache_path = Path(
            '/'.join(
                (__file__, '../../data/cache/aligner/name_index.json'))).resolve()
        try:
            os.remove(cache_path)
        except FileNotFoundError:
            pass
        aligner = Aligner()
        nidx = (
            'https://raw.githubusercontent.com/ryanfb/pleiades-geojson/'
            'gh-pages/name_index.json')
        content, fetched = aligner._fetch_file(nidx, cache_override=True)
        assert_true(fetched)
        content, fetched = aligner._fetch_file(nidx, cache_override=False)
        assert_false(fetched)
        content, fetched = aligner._fetch_file(nidx, cache_override=True)
        assert_true(fetched)
        content, fetched = aligner._fetch_file(nidx)
        assert_false(fetched)
        j = json.loads(content)
        assert_true(isinstance(j, list))
        assert_equal(2, len(j[0]))


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

