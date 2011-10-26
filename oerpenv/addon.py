# -*- coding: utf-8 -*-
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

from os.path import abspath, basename, dirname, join
import os

class Addon:
        def __init__(self, addon_config_path):
                """
                Init an addon class information 
                """
                self.config_path = abspath(addon_config_path)
                self.path = dirname(self.config_path)
                self._token = basename(self.path)
                self._description = None

        def read_description(self):
                """
                Read Addon file description.
                """
                if self._description is None:
                        self._description = eval(open(self.config_path).read())

        @property
        def token(self):
                """
                Return addon name.
                """
                return self._token

        @property
        def name(self):
                """
                Return addon short description.
                """
                self.read_description()
                return self._description['name']

        @property
        def description(self):
                """
                Return addon long description.
                """
                self.read_description()
                return self._description['description']

        @property
        def depends(self):
                """
                Return addon list with the addon depends.
                """
                self.read_description()
                return self._description['depends']

        @property
        def website(self):
                """
                Return the website of the addon.
                """
                self.read_description()
                if 'website' in self._description:
                    return self._description['website']
                else:
                    return None

        @property
        def author(self):
                """
                Return the author of the addon.
                """
                self.read_description()
                return self._description['author']

        @property
        def version(self):
                """
                Return the version of the addon.
                """
                self.read_description()
                return self._description['version']

        @property
        def objects(self):
                """
                Return a duple with a list of objects declared and inherited in the addon.
                """
                import re
                namesearch = re.compile(r'^\s*_name\s*=\s*["\']([a-z][\w\.]*)["\']')
                inheritsearch = re.compile(r'^\s*_inherit\s*=\s*["\']([a-z][\w\.]*)["\']')
                search_files = set([])

                for p, ds, fs in os.walk(self.path):
                        search_files.update(set([ join(p,f) for f in fs if f[-3:]=='.py']))

                objects = set()
                inherited = set()
                for filename in search_files:
                        with open(filename) as file:
                                lines = file.readlines()
                                namematchs = [ namesearch.search(line) for line in lines ]
                                inheritmatchs = [ inheritsearch.search(line) for line in lines ]
                                objects.update([ match.group(1) for match in namematchs if match != None ])
                                inherited.update([ match.group(1) for match in inheritmatchs if match != None ])
                return objects - inherited, inherited

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
