#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Align my gaz entries to the Pleiades gazetteer of ancient places
"""

from datetime import datetime, timedelta
import json
import logging

from textnorm import normalize_space, normalize_unicode
from mygaz.alignment.aligner import Aligner
import os
from pathlib import Path
import requests

NAMES_INDEX_URI = (
    'https://raw.githubusercontent.com/ryanfb/pleiades-geojson/'
    'gh-pages/name_index.json')

logger = logging.getLogger(__name__)


class PleiadesAligner(Aligner):

    def __init__(self):
        self.cache_name = __name__.lower().split('.')[-1]
        self.cache_path = Path(
            '/'.join(
                (__file__, '../../../data/cache/', self.cache_name))).resolve()
        self.lookups = {
            'name_keys': {},
            'name_strings': {}
        }
        Aligner.__init__(self)

    def _initialize_lookup_name_keys(self, rebuild=False):
        file_path = self.cache_path / 'name_keys.json'
        if not rebuild:
            try:
                content = self._read_from_cache(file_path)
            except FileNotFoundError:
                pass
            else:
                self.lookups['name_keys'] = json.loads(content)
                return
        idx = self._get_names_index()
        d = {}
        for name_string, pid in idx:
            k = self._make_name_key(name_string)
            try:
                d[k]
            except KeyError:
                d[k] = []
            d[k].append(pid)
        self.lookups['name_keys'] = d
        content = json.dumps(d, ensure_ascii=False, indent=4, sort_keys=True)
        self._save_to_cache(bytes(content, encoding='utf-8'), file_path)

    def _initialize_lookup_name_strings(self, rebuild=False):
        file_path = self.cache_path / 'name_strings.json'
        if not rebuild:
            try:
                content = self._read_from_cache(file_path)
            except FileNotFoundError:
                pass
            else:
                self.lookups['name_strings'] = json.loads(content)
                return
        idx = self._get_names_index()
        d = {}
        for name_string, pid in idx:
            k = normalize_space(normalize_unicode(name_string))
            try:
                d[k]
            except KeyError:
                d[k] = []
            d[k].append(pid)
        self.lookups['name_strings'] = d
        content = json.dumps(d, ensure_ascii=False, indent=4, sort_keys=True)
        self._save_to_cache(bytes(content, encoding='utf-8'), file_path)

    def _get_names_index(self):
        try:
            self._names_index
        except AttributeError:
            content, fetched = self._fetch_file(NAMES_INDEX_URI)
            self._names_index = json.loads(content)
        return self._names_index


