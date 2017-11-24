#!/usr/bin/env python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name="jawa",
    packages=find_packages(),
    version="1.1",
    description="Doing fun stuff with JVM ClassFiles.",
    author="Tyler Kennedy",
    author_email="tk@tkte.ch",
    url="http://github.com/TkTech/Jawa",
    keywords=["java", "disassembly", "disassembler"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Disassemblers"
    ],
    install_requires=[
        'click>=5.0',
        'six'
    ],
    tests_require=[
        'pytest>=2.10',
    ],
    extras_require={
        'dev': [
            'pytest',
            'sphinx',
            'sphinxcontrib-googleanalytics',
            'sphinx_rtd_theme',
            'ghp-import'
        ]
    },
    entry_points='''
    [console_scripts]
    jawa=jawa.cli:cli
    '''
)
