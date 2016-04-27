# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from setuptools import setup
import re

version = ''
with open('pyticketswitch/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='pyticketswitch',
    version=version,
    author='Ingresso',
    author_email='systems@ingresso.co.uk',
    url='https://github.com/ingresso-group/pyticketswitch/',
    packages=[
        'pyticketswitch',
        'pyticketswitch.interface_objects'
    ],
    license='MIT',
    description='A Python interface for the Ingresso XML Core API',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests>=2.0.0',
        'six',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
)
