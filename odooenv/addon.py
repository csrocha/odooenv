# -*- coding: utf-8 -*-
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

from os.path import abspath, basename, dirname, join, exists, lexists, realpath
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
            return self._description.get('description','')

        @property
        def depends(self):
            """
            Return addon list with the addon depends.
            """
            self.read_description()
            return self._description.get('depends',[])

        @property
        def website(self):
            """
            Return the website of the addon.
            """
            self.read_description()
            return self._description.get('website',None)

        @property
        def author(self):
            """
            Return the author of the addon.
            """
            self.read_description()
            return self._description.get('author',None)

        @property
        def version(self):
            """
            Return the version of the addon.
            """
            self.read_description()
            return self._description.get('version',None)

        def environment_path(self, environment):
            """
            Return the path of the addon in the environment.
            """
            addons_path = environment.get_addonsourcepath()
            return join(addons_path, self.token)

        def is_enable(self, environment):
            """
            Return true if the addon is enabled in the environment.
            """
            path = self.environment_path(environment)
            return exists(path) and exists(realpath(path)) and dirname(realpath(path)) != self.path

        def is_saned(self, environment):
            """
            Return true if the addon is saned.
            """
            path = self.environment_path(environment)
            return lexists(path) and os.path.exists(realpath(path)) or not lexists(path)

        def enable(self, environment, force=False):
            """
            Enable this addon in this environment. Not check depends.
            """
            addons_path = environment.get_addonsourcepath()
            where_install = join(addons_path, self.token)
            is_enabled = self.is_enable(environment)
            is_saned = self.is_saned(environment)
            is_exists = os.path.exists(where_install)
            is_link = os.path.islink(where_install)

            if is_link:
                if ((is_exists and force) or \
                    (is_enabled and force) or \
                    (not is_saned)):
                    os.remove(where_install)
                elif is_enabled and not force:
                    return False

            if not os.path.exists(where_install):
                os.symlink(self.path, where_install)

            return True

        def disable(self, environment, force=False):
            """
            Disable this addon in this environment. Not check depends.
            """
            addons_path = environment.get_addonsourcepath()
            where_install = join(addons_path, self.token)
            if self.is_enable(environment):
                os.remove(where_install)
                return True
            elif not self.is_enable(environment) and force:
                return True
            return False

        @property
        def objects(self):
            """
            Return a duple with a list of objects declared and inherited in the addon.
            """
            import re
            objects = set()
            inherited = set()
            for filename, name, match in self.search( 
                {'object':re.compile(r'^\s*_name\s*=\s*["\']([a-z][\w\.]*)["\']'),
                 'inherit':re.compile(r'^\s*_inherit\s*=\s*["\']([a-z][\w\.]*)["\']'),},
                re.compile(r'^.*\.py$')
            ):
                if name == 'object':
                    objects.update(match)
                else:
                    inherited.update(match)
            return objects - inherited, inherited

        @property
        def entities(self):
            """
            Return a list of entities declared in xml.
            """
            import re
            record = set()
            items = {}
            for filename, name, match in self.search( 
                {'record':re.compile(r'id\s*=\s*["\']([^"]*)["\']'), },
                re.compile(r'^.*\.xml$')
            ):
                if name == 'record':
                    record.update(match)
            return record

        def entity(self, entity):
            """
            Return a entity information.
            """
            import re
            record = set()
            items = {}
            for filename, name, match in self.search( 
                {'record':re.compile(r'id\s*=\s*["\']([^"]*)["\']'), },
                re.compile(r'^.*\.xml$')
            ):
                if name == 'record' and entity in match:
                    yield filename

        def search(self, re_patterns, re_file):
            """
            Search in files
            """
            search_files = set()
            for p, ds, fs in os.walk(self.path):
                    search_files.update(set([ join(p,f) for f in fs if re_file.search(f)]))

            for filename in search_files:
                with open(filename) as file:
                    lines = file.readlines()
                    for re_name, re_pattern in re_patterns.items():
                        matchs = [ re_pattern.search(line) for line in lines ]
                        matchs = [ match.group(1) for match in matchs if match != None ]
                        if len(matchs) > 0:
                            yield filename, re_name, matchs

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
