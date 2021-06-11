#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Covert a list of placenames to a simple gazetteer
"""

from airtight.cli import configure_commandline
import json
import logging
import magic
from pathlib import Path
import regex as re
from textnorm import normalize_space, normalize_unicode

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
    ['-e', '--encoding', 'utf-8', 'text encoding', False],
    ['-o', '--output', 'json', 'output format', False]
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
    ['input', str, 'path to input file'],
]


def parse_txt(inpath, encoding):
    logger.info(
        'Parsing txt file with encoding={}: {}'.format(
            encoding, str(inpath)))
    lines = []
    with open(inpath, 'r', encoding=encoding) as f:
        lines = f.readlines()
    del f
    logger.debug(
        'Read {} lines from {}'.format(
            len(lines), inpath))
    return lines


def parse_plaintext(inpath, encoding):
    suffix = inpath.suffix
    if suffix == '.txt':
        return parse_txt(inpath, encoding)
    else:
        raise NotImplementedError(
            'Unsupported file type ({}): {}'.format(
                suffix[1:], str(inpath)))


def process_names(names_raw, **kwargs):
    names_cooked = [
        normalize_unicode(normalize_space(n), target='NFC') for n in names_raw]
    names_cooked = [n for n in list(set(names_cooked)) if n != '']
    keys = {}
    for n in names_cooked:
        key = ''.join(rx_punct.sub('', n.lower()).split())
        if key == '':
            logger.error(
                'Skipping entry "{}" because its key is a zero-length string.'
                ''.format(n))
            continue
        try:
            keys[key]
        except KeyError:
            keys[key] = [n]
        else:
            if n not in keys[key]:
                keys[key].append(n)
    return keys


def output(data, format):
    if format == 'plain':
        for k, names in data.items():
            print('{}: ["{}"]'.format(
                k, '", "'.join(sorted(names))))
    elif format == 'json':
        outd = {}
        for k in sorted(data.keys()):
            outd[k] = {'names': data[k]}
        print(json.dumps(outd, ensure_ascii=False, indent=4))
    else:
        logger.error(
            'Output format "{}" is not defined. Using "plain".'.format(format))
        output(data, 'plain')


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    inpath = Path(kwargs['input']).expanduser().resolve(strict=True)
    inmime = magic.from_file(str(inpath), mime=True)
    if inmime == 'text/plain':
        names = parse_plaintext(inpath, kwargs['encoding'])
    else:
        raise NotImplementedError(
            'Unsupported file type ({}): {}'.format(
                inmime, str(inpath)))
    results = process_names(names, **kwargs)
    output(results, kwargs['output'])
    


if __name__ == "__main__":
    main(**configure_commandline(
        OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
