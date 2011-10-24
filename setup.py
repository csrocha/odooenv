#!/usr/bin/env python

from distutils.core import setup

setup(name='oerpenv',
            version='1.0',
            description='OpenERP Environment Administrator',
            author='Cristian S. Rocha',
            author_email='cristian.rocha@moldeointeractive.com.ar',
            url='http://www.moldeointeractive.com.ar/',
            packages=['oerpenv'],
            scripts=['scripts/oerpenv'],
           )

