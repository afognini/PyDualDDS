#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2017 Andreas Fognini
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PyDualDDS",
    version = "0.0.1",
    author = "Andreas Fognini",
    author_email = "a.w.fognini@tudelft.nl",
    description = ("PyDuyalDDS installer."),
    license = "GPLv3",
    keywords = "DDS, Sine, Frequency, Phase, Synthesizer",
    py_modules =["PyDualDDS"],
    setup_requires=[],
    install_requires=['pyftdi'],
    long_description=read('README.md'),
    #test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
