#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Align my gaz entries to the Pleiades gazetteer of ancient places
"""

from datetime import datetime, timedelta
import json
import logging
import os
from pathlib import Path
import requests

NAMES_INDEX_URI = (
    'https://raw.githubusercontent.com/ryanfb/pleiades-geojson/'
    'gh-pages/name_index.json')

logger = logging.getLogger(__name__)


class PleiadesAligner:

    def __init__(
        self,
        cache_duration=CACHE_DURATION_DEFAULT,
        cache_override=False
    ):
        self.cache_duration = cache_duration
        self.cache_override = False
        self.lookups = {
            'name_keys': {},
            'name_strings': {}
        }
        self._initialize_lookups()

    def _initialize_lookups(self):
        self.names_index, fetched = self._fetch_names_index()
        for k in self.lookups.keys():
            getattr(self, '_initialize_lookup_' + k)(rebuild=fetched)

    def _initialize_lookup_name_keys(self, rebuild=False):
        pass

    def _initialize_lookup_name_strings(self, rebuild=False):
        pass

    def _fetch_names_index(self, cache_override=False):
        # get a recent copy of Ryan Baumann's pleiades names index
        cachepath = Path(
            '/'.join(
                (__file__, '../../../data/cache/name_index.json'))).resolve()
        if cache_override:
            fetch = True
        else:
            fetch = False
            try:
                modified = datetime.fromtimestamp(os.stat(cachepath).st_mtime)
            except FileNotFoundError:
                fetch = True
            else:
                now = datetime.today()
                max_delay = self.cache_duration
                if now - modified > max_delay:
                    fetch = True
                else:
                    logger.info(
                        'Locally cached version of Pleiades names index is being '
                        'used.')
        if fetch:
            r = requests.get(NAMES_INDEX_URI)
            names_index = r.json()
            with open(cachepath, 'w', encoding='utf-8') as f:
                json.dump(names_index, f, ensure_ascii=False, indent=4)
            del f
            logger.info(
                'Fetched latest version of the Pleiades names index file and '
                'saved to {} for future use'.format(cachepath))
        else:
            with open(cachepath, 'r', encoding='utf-8') as f:
                names_index = json.load(f)
            del f
        return names_index, fetch
