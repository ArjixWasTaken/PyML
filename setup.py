#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='PyML',
    version="0.0.3",
    author='Arjix',
    author_email='arjixg53@gmail.com',
    description='A python HTML builder library.',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    url='https://github.com/ArjixWasTaken/PyML',
    keywords=['html', 'html builder'],
    install_requires=["bs4"],
    extras_require={},
    long_description=long_description,
    long_description_content_type='text/markdown'
)
