#!/usr/bin/env python

from setuptools import setup

setup(name='oerpenv',
      version='1.0',
      description='OpenERP Environment Administrator',
      author='Cristian S. Rocha',
      author_email='cristian.rocha@moldeointeractive.com.ar',
      url='http://www.moldeointeractive.com.ar/',
      scripts=['scripts/oerpenv'],
      packages=['oerpenv'],
      test_suite='tests',
      install_requires=['virtualenv','bzrlib','pysvn','psycopg2'],
   )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
