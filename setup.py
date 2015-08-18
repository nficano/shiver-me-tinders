#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shiver_me_tinders import __version__
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

setup(
    name='ShiverMeTinders',
    version=__version__,
    packages=['shiver_me_tinders'],
    description='A lightweight wrapper around the Tinder undocumented API.',
    author='Nick Ficano',
    author_email='nficano@gmail.com',
    url='https://github.com/nficano/shiver-me-tinders',
    download_url='https://github.com/nficano/shiver-me-tinders/tarball/0.0.3',
    keywords=['tinder'],
    license=open_file('LICENSE.txt').read(),
    install_requires=['requests', 'PyYAML'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Internet"
    ],
    zip_safe=True
)
