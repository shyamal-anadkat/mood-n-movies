# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='AIPI540 NLP Project',
    long_description=readme,
    author='Shyamal Anadkat',
    author_email='sha18@duke.edu',
    url='https://github.com/shyamal-anadkat/AIPI540_NLP',
    license=license,
    packages=find_packages(exclude=('data', 'docs', 'notebooks'))
)