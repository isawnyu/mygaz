#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test gazetteer aligment"""

from datetime import datetime, timedelta
import json
import logging
from mygaz.alignment.aligner import Aligner
from mygaz.alignment.pleiades import PleiadesAligner
from nose.tools import assert_equal, assert_false, assert_true, raises
import os
from pathlib import Path
import shutil
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

    def setUp(self):
        cache_path = Path(
            '/'.join(
                (__file__, '../../data/cache/aligner'))).resolve()
        shutil.rmtree(cache_path, ignore_errors=True)

    def test_init(self):
        aligner = Aligner()

    def test_fetch(self):
        aligner = Aligner()
        nidx = (
            'https://raw.githubusercontent.com/ryanfb/pleiades-geojson/'
            'gh-pages/name_index.json')

        # first fetch: cache is empty (see self.setUp) so get from web
        cache_path = Path(
            '/'.join(
                (__file__, '../../data/cache/aligner/name_index.json'))).resolve()
        assert_false(cache_path.exists())
        content, fetched = aligner._fetch_file(nidx)
        assert_true(fetched)
        assert_true(cache_path.is_file())

        # second fetch: cache is available, so use it
        content, fetched = aligner._fetch_file(nidx, cache_override=False)
        assert_false(fetched)

        # ensure cache override works
        content, fetched = aligner._fetch_file(nidx, cache_override=True)
        assert_true(fetched)

        # ensure stale cache re-download works
        now = datetime.today()
        max_delay = aligner.cache_duration
        when = now - max_delay * 2
        when_epoch = when.timestamp()
        os.utime(cache_path, (when_epoch, when_epoch))
        content, fetched = aligner._fetch_file(nidx)
        assert_true(fetched)

        # make sure the content survived the process
        j = json.loads(content)
        assert_true(isinstance(j, list))
        assert_equal(2, len(j[0]))
    
    def test_fetch_rename(self):
        cache_path = Path(
            '/'.join(
                (__file__, '../../data/cache/aligner/foo.json'))).resolve()
        aligner = Aligner()
        nidx = (
            'https://raw.githubusercontent.com/ryanfb/pleiades-geojson/'
            'gh-pages/name_index.json')
        content, fetched = aligner._fetch_file(nidx, cache_override=True, name_override='foo.json')
        assert_true(fetched)
        assert_true(cache_path.is_file())


class Test_PleiadesAlignment(TestCase):

    def setUp(self):
        self.aligner = PleiadesAligner()

    def tearDown(self):
        """Change me"""
        del self.aligner

    def test_foo(self):
        a = self.aligner
        assert_equal(2, len(a.lookups))
        assert_true('name_strings' in a.lookups.keys())
        assert_true('name_keys' in a.lookups.keys())
        assert_true('roma' in a.lookups['name_keys'].keys())
        assert_true('Roma' in a.lookups['name_strings'].keys())