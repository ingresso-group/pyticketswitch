#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import subprocess
import sys

import six
from flake8.main import main as flake8_main
from libmodernize.main import main as libmodernize_main


CODE_PATHS = [
    'lint.py',
    'pyticketswitch',
    'tests',
]


def main():
    exit_on_failure(run_flake8())
    exit_on_failure(run_modernize())
    exit_on_failure(run_isort())


def run_flake8():
    print('Running flake8 code linting')
    try:
        original_argv = sys.argv
        sys.argv = ['flake8'] + CODE_PATHS
        did_fail = False
        flake8_main()
    except SystemExit:
        did_fail = True
    finally:
        sys.argv = original_argv

    if did_fail:
        print('flake8 failed')
    else:
        print('flake8 passed')
    return did_fail


def run_modernize():
    print('Running modernize checks')
    try:
        orig_stdout = getattr(sys, 'stdout')
        out = six.StringIO()
        setattr(sys, 'stdout', out)
        libmodernize_main(CODE_PATHS)
    finally:
        sys.stdout = orig_stdout
    output = out.getvalue()
    print(output)
    ret = len(output)
    if ret:
        print('modernize failed')
    else:
        print('modernize passed')
    return ret


def run_isort():
    print('Running isort check')
    return subprocess.call([
        'isort', '--recursive', '--check-only', '--diff',
        '-a', 'from __future__ import absolute_import, print_function, division, unicode_literals',
    ] + [x for x in CODE_PATHS if x != 'tests'])


def exit_on_failure(ret):
    if ret:
        sys.exit(ret)


if __name__ == '__main__':
    main()
