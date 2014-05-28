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
      version='1.8.8',
      author='Cristian S. Rocha',
      author_email='cristian.rocha@moldeo.coop',
      maintainer='Cristian S. Rocha',
      maintainer_email='cristian.rocha@moldeo.coop',
      url='http://business.moldeo.coop/',
      description='OpenERP Environment Administrator',
      long_description="""
      OERPenv helps you manage virtual python environments with different OpenERP servers.
      It's make easy to develop, migrate and maintain different versions of OpenERP servers in the same hardware box.

      This package installs command 'oerpenv' with these sub-commands:

      $ oerpenv -h
      usage: oerpenv [-h]
                     
                     {restore,web-stop,show,server-start,activate,pip,shell-db,web-start,create,add,init,server-stop,create-db,test,search-entity,init-db,enable,csv2xml,update,disable,search-object,list-installables,dummy,drop-db,setup,list-addons,client,list-db,install,snapshot}
                     ...

      optional arguments:
        -h, --help            show this help message and exit

      subcommands:
        The OpenERP environment administrator help you to administrate OpenERP
        environments. You can use the following commands.

        {restore,web-stop,show,server-start,activate,pip,shell-db,web-start,create,add,init,server-stop,create-db,test,search-entity,init-db,enable,csv2xml,update,disable,search-object,list-installables,dummy,drop-db,setup,list-addons,client,list-db,install,snapshot}
                              commands
          init                Init an environment in the work path or in the
                              declared path.
          setup               Init an environment in the work path or in the
                              declared path.
          update              Update sources.
          create              Create a new python environment.
          add                 Add a branch with to the sources list.
          install             Install all software in the default environment of in
                              the declared.
          list-installables   List all availables applications in sources.
          list-addons         List availables addons in sources. Show all addons if
                              not filter expression declared.
          enable              Enabel addons on the environment. Create a symbolic
                              link.
          disable             Disable addons on the environment. Remove a symbolic
                              link.
          dummy               Create a dummy addon. Useful to create new addon.
          test                Execute the server in test mode for this addon.
          client              Execute the server in test mode for this addon.
          server-start        Start the server.
          server-stop         Stop the server.
          web-start           Start the web client.
          web-stop            Stop the web client.
          search-object       Search addons with this object.
          search-entity       Search in xml some declared entity with id
          show                Show addon information.
          list-db             List availables databases.
          shell-db            Execute a shell for sql commands over the database.
          create-db           Create a void database.
          drop-db             Remove a database.
          init-db             Prepare a minimalistic OpenERP database.
          snapshot            Generate a database snapshot.
          restore             Restore a database snapshot.
          pip                 Install Python packages in the virtual environment.
          csv2xml             Convert CSV files to an XML files.
          activate            Active bash instance in virtual environment.

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
      scripts=['scripts/oerpenv'],
      packages=['oerpenv'],
      test_suite='tests',
      install_requires=['virtualenv','psycopg2','argparse','bzr'],
      dependency_links=['http://pysvn.barrys-emacs.org/source_kits/pysvn-1.7.5.tar.gz'],
   )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
