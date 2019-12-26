#!/usr/bin/env python

from setuptools import setup, find_packages
import io
import os
import sys
import re
import shutil

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = io.open(os.path.join(package, '__init__.py'), encoding='utf-8').read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

def read_all(f):
    with io.open(f, encoding="utf-8") as I:
        return I.read()

requirements = map(str.strip, open("requirements.txt").readlines())

version = get_version('rejson')

if sys.argv[-1] == 'publish':
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('rejson.egg-info')
    sys.exit()

setup(name='rejson',
      version=version,
      description='ReJSON Python Client',
      long_description=read_all("README.md"),
      long_description_content_type='text/markdown',
      classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: BSD License',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Development Status :: 4 - Beta',
            'Topic :: Database',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ],  # Get from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Redis JSON Extension',
      author='RedisLabs',
      author_email='oss@redislabs.com',
      url='http://github.com/RedisLabs/rejson-py',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
