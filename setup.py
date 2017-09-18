#!/usr/bin/env python

from distutils.core import setup

install_requires = [
    'PyYAML==6.7'
    ]

setup(name='yaml2xml',
      version='1.0',
      description='convert between yaml and xml',
      author='hejack0207',
      author_email='hejack0207@sina.com',
      url='https://github.com/hejack0207/yaml2xml',
      packages=['yaml2xml'],
      package_dir = {'': 'lib'},
      requires=install_requires,
      scripts=['bin/pysqlcli'],
     )
