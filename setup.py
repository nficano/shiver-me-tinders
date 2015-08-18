#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

setup(
    name='shiver_me_tinders',
    version="0.1.1",
    packages=['shiver_me_tinders'],
    description="A lightweight wrapper around Tinder's API.",
    author='Nick Ficano',
    author_email='nficano@gmail.com',
    url='https://github.com/nficano/shiver-me-tinders',
    download_url='https://github.com/nficano/shiver-me-tinders/tarball/0.1.1',
    keywords=['tinder'],
    license=open_file('LICENSE.txt').read(),
    install_requires=[
        'requests>=2.7.0',
        'PyYAML>=3.11'
    ],
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
