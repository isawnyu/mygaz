#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Align a mygaz to Pleiades
"""

from airtight.cli import configure_commandline
from copy import deepcopy
from datetime import datetime, timedelta

import json
import logging
from mygaz.alignment.pleiades import PleiadesAligner
import os
from pathlib import Path
from pprint import pprint
import regex as re
import requests
import sys
from textnorm import normalize_space, normalize_unicode
import textwrap
import time


logger = logging.getLogger(__name__)
rx_punct = re.compile(r'[\p{Punctuation}\p{Other}]+')

DEFAULT_LOG_LEVEL = logging.INFO
OPTIONAL_ARGUMENTS = [
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
        False],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)',
        False],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)', False],
    ['-f', '--fuzzy', False, 'use fuzzy name matching if no exact matches', False]
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
    ['input', str, 'path to mygaz json file']
]


def find_candidates(mygaz, fuzzy):
    logger.info('Initializing Pleiades Aligner')
    aligner = PleiadesAligner()
    logger.info('Attempting alignment ...')
    agaz = {}
    i = 0
    for k, data in mygaz.items():
        i += 1
        if i % 10 == 0:
            logger.info(
                '... processed {} of {} entries in gazetteer'
                ''.format(i, len(mygaz)))
        results = []
        if len(data['names']) != 1:
            continue
        for name in data['names']:
            results.append(aligner.match_name(name, fuzzy_matching=False))
        if len(results) == 1:
            m = results[0]['matches']
            i_consensus = len(m['consensus'])
            i_keys = len(m['name_keys'])
            i_strings = len(m['name_strings'])
            if fuzzy and i_consensus == 0 and i_keys == 0 and i_strings == 0:
                results[0] = aligner.match_name(name, fuzzy_matching=True)
                m = results[0]['matches']
                i_consensus = len(m['consensus'])
                i_keys = len(m['name_keys'])
                i_strings = len(m['name_strings'])
                i_fuzzy = len(results[0]['matches_fuzzy']['pids'])
            else:
                i_fuzzy = 0
            agaz[k] = deepcopy(data)
            if i_consensus == 1 and i_keys == 1 and i_strings == 1:
                agaz[k]['sameas'] = m['consensus']
                agaz[k]['closematch'] = []
            elif i_consensus == 1:
                agaz[k]['sameas'] = m['consensus']
                agaz[k]['closematch'] = [item for item in list(set(m['name_keys']).union(set(m['name_strings']))) if item != m['consensus']]
            elif i_consensus > 0 or i_keys > 0 or i_strings > 0:
                agaz[k]['sameas'] = []
                agaz[k]['closematch'] = list(set(m['consensus']).union(set(m['name_strings']), set(m['name_keys'])))
            elif i_fuzzy > 0:
                agaz[k]['sameas'] = []
                agaz[k]['closematch'] = results[0]['matches_fuzzy']['pids']
            else:
                agaz[k]['sameas'] = []
                agaz[k]['closematch'] = []
        else:
            raise NotImplementedError('multiple names: {}'.format(data['names']))

    return agaz

def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    inpath = Path(kwargs['input']).expanduser().resolve(strict=True)
    with open(inpath, 'r', encoding='utf8') as f:
        mygaz = json.load(f)
    del f
    logger.info(
        'Read {} place entries from {}'.format(len(mygaz), inpath))
    agaz = find_candidates(mygaz, kwargs['fuzzy'])
    misses = []
    hits = []
    candidates = []
    for k, data in agaz.items():
        if len(data['sameas']) == 0 and len(data['closematch']) == 0:
            misses.append(k)
        elif len(data['sameas']) == 1 and len(data['closematch']) == 0:
            hits.append(k)
        else:
            candidates.append(k)
    logger.info('{} misses'.format(len(misses)))
    logger.info('{} hits'.format(len(hits)))
    logger.info('{} candidates'.format(len(candidates)))
    print(json.dumps(agaz, ensure_ascii=False, indent=4, sort_keys=True))


if __name__ == "__main__":
    main(**configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
