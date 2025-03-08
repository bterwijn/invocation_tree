# This file is part of invocation_tree.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description_from_readme = (this_directory / "README.md").read_text()

setup(
    name = 'invocation_tree',
    version = '0.0.12',
    description = 'Generate an invocation tree of functions calls.',
    long_description = long_description_from_readme,
    long_description_content_type = 'text/markdown',
    readme = 'README.md',
    url = 'https://github.com/bterwijn/invocation_tree',
    author = 'Bas Terwijn',
    author_email = 'bterwijn@gmail.com',
    license = 'BSD 2-clause',
    packages = ['invocation_tree'],
    install_requires = ['graphviz'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Software Development :: Debuggers',
    ],
)
