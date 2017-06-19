# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pyticketswitch',
    version='2.0.4',
    author='Ingresso',
    author_email='systems@ingresso.co.uk',
    url='https://github.com/ingresso-group/pyticketswitch/',
    packages=[
        'pyticketswitch',
    ],
    license='MIT',
    description='A Python interface for the Ingresso F13 API',
    install_requires=[
        'requests>=2.0.0',
        'python-dateutil>2.5.3',
        'six>=1.10.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
)
