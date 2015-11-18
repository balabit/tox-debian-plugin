# Copyright (c) 2015 BalaBit
# All Rights Reserved.

from setuptools import setup

setup(
    name='tox-DEBIAN',
    description='debian package installer tox plugin',
    license="MIT license",
    version='0.1',
    py_modules=['tox_DEBIAN'],
    entry_points={'tox': ['DEBIAN = tox_DEBIAN']},
    install_requires=['tox>=2.0'],
)
