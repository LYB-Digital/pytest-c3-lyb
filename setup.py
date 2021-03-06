#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-c3-lyb',
    version='0.1.0',
    author='James Trousdale',
    author_email='james.trousdale@lyondellbasell.com',
    maintainer='James Trousdale',
    maintainer_email='james.trousdale@lyondellbasell.com',
    license='MIT',
    url='https://github.com/james-trousdale-lyb/pytest-c3-lyb',
    description='C3 connector plugin for pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_c3_lyb'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'c3-lyb = pytest_c3_lyb',
        ],
    },
)
