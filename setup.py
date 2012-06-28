#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from distutils.core import setup
import os


def read_file(name):
    return codecs.open(os.path.join(os.path.dirname(__file__), name), encoding='utf-8').read()


setup(
    author='Mike Johnson',
    author_email='mike@mrj0.com',
    name='vinyl',
    description='Mutable record type for dealing with flat files like CSV or pipe-delimited data',
    long_description=read_file('README.rst'),
    version='0.4',
    url='https://github.com/mrj0/vinyl/',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        ],
    packages=['vinyl'],
    )
