#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='rejson',
    version='0.1',
    author='Redis Labs',
    author_email='oss@redislabs.com',
    description='ReJSON Python Client',
    url='http://github.com/RedisLabs/rejson-py',
    packages=find_packages(),
    install_requires=['redis', 'hiredis', 'rmtest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
    ]
)