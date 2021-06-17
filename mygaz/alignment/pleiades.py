#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Align my gaz entries to the Pleiades gazetteer of ancient places
"""

from datetime import datetime, timedelta
import json
import logging
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
        self.lookups = {
            'name_keys': {},
            'name_strings': {}
        }
        Aligner.__init__(self)

    def _initialize_lookup_name_keys(self, rebuild=False):
        pass

    def _initialize_lookup_name_strings(self, rebuild=False):
        pass

