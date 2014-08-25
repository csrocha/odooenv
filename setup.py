#!/usr/bin/env python
##############################################################################
#
#    OdooEnv, Odoo Environment Administrator
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

setup(name='odooenv',
      version='2.0.11',
      author='Cristian S. Rocha',
      author_email='cristian.rocha@moldeo.coop',
      maintainer='Cristian S. Rocha',
      maintainer_email='csr@moldeo.coop',
      url='http://biz.moldeo.coop/',
      description='Odoo Environment Manager',
      long_description="""
      OdooEnv helps you manage virtual python environments with different Odoo servers.
      It's make easy to develop, migrate and maintain different versions of Odoo servers in the same hardware box.
      """,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2.6',
          'Topic :: Software Development :: Build Tools',
      ],
      scripts=['scripts/odooenv'],
      packages=['odooenv'],
      package_dir={'odooenv': 'odooenv'},
      package_data={'odooenv': ['data/*.yml']},
      test_suite='tests',
      install_requires=['virtualenv','psycopg2','argparse','bzr','pyyaml'],
      dependency_links=['http://pysvn.barrys-emacs.org/source_kits/pysvn-1.7.5.tar.gz'],
   )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
