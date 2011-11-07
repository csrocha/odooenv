#!/usr/bin/env python
##############################################################################
#
#    OERPEnv, OpenERP Environment Administrator
#    Copyright (C) 2011-2015 Coop Trab Moldeo Interactive 
#    (<http://www.moldeointeractive.com.ar>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


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
      install_requires=['virtualenv','psycopg2','argparse'],
      #install_requires=['virtualenv','bzrlib','pysvn','psycopg2'],
   )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
