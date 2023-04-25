#!/usr/bin/env python
# pylint: disable= missing-module-docstring
from setuptools import setup

setup(
    name='trainings',
    version='1.0',
    description='Service to interact with trainings',
    author='Grupo 5',
    packages=[''],
    include_package_data=True,
    exclude_package_data={'': ['tests', 'kubernetes']},
)
