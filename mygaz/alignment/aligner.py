#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base aligment class
"""

from datetime import datetime, timedelta
import logging
import os
from pathlib import Path
from pathvalidate import sanitize_filename
import requests
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

CACHE_DURATION_DEFAULT = timedelta(hours=24)

class Aligner:
    """Base class for gazetteer alignment"""

    def __init__(
        self,
        cache_duration=CACHE_DURATION_DEFAULT,
        cache_override=False
    ):
        self.cache_name = __name__.lower().split('.')[-1]
        self.cache_path = Path(
            '/'.join(
                (__file__, '../../../data/cache/', self.cache_name))).resolve()
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.cache_duration = cache_duration
        self.cache_override = False
        self._initialize_downloads()
        try:
            self.lookups  # define in subclass
        except AttributeError:
            self.lookups = {}
        self._initialize_lookups()

    def _initialize_downloads(self):
        """Download/update basic data and indexes"""
        # override in child class to get basic data and indexes 
        pass

    def _initialize_lookups(self):
        """Initialize lookup indices and tables"""
        for k in self.lookups.keys():
            getattr(self, '_initialize_lookup_' + k)(rebuild=fetched)

    def _fetch_file(self, uri, cache_override=False, name_override=''):
        """Get a file from cache or web as appropriate"""
        if name_override != '':
            filename = name_override
        else:
            parts = urlsplit(uri)
            filename = parts.path.split('/')[-1]
        filename = sanitize_filename(filename)
        filepath = self.cache_path / filename
        if cache_override:
            fetch = True
        else:
            fetch = False
            try:
                modified = datetime.fromtimestamp(os.stat(filepath).st_mtime)
            except FileNotFoundError:
                fetch = True
            else:
                now = datetime.today()
                max_delay = self.cache_duration
                if now - modified > max_delay:
                    fetch = True
        if fetch:
            r = requests.get(uri)
            content = r.content
            self._save_to_cache(content, filepath)
        else:
            content = self._read_from_cache(filepath)
        return content, fetch

    def _save_to_cache(self, content, filepath):
        """Save content to a file in cache"""
        with open(filepath, 'wb') as f:
            f.write(content)
        del f

    def _read_from_cache(self, filepath):
        """Load content from a file in cache"""
        with open(filepath, 'rb') as f:
            content = f.read()
        del f
        return content


    