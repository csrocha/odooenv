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

import re
import virtualenv
import sys
import time
import logging
import logging.config
from os import makedirs, walk, symlink, mkdir, listdir
from os.path import abspath, join, exists, lexists, dirname, basename
from installable import Installable
from odooenv import tools
from odooenv.defaults import defaults
from virtualenv import subprocess
from addon import Addon
from repository import Repository
from pwd import getpwnam
from urllib import urlretrieve

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

config_filename = 'environment.yml'

class NoEnvironmentConfigFileError(RuntimeError):
    def __init__(self, filepath):
        self.filepath = filepath
        self.message = "No environment config file available (%s)" % filepath

class NoVersionAvailableError(RuntimeError):
    def __init__(self, version):
        self.version = version
        self.message = "No version available (%s)" % version

class OdooEnvironment:
    def __init__(self, path="."):
        """
        Create an instance of OdooEnvironment class.

        Arguments:
        config_filename -- Full path to the configuration file.
        """
        self.config_filename = abspath(join(path, 'etc', config_filename))
        self.root_path = abspath(path)
        self.load()

    def setup(self):
        # Create all nescesary dirs
        for d in [ join(self.root_path, d) for d in self._config.take(['dir'])['dir']]:
            if not exists(d): makedirs(d)

    def load(self):
        """
        Load configuration file.
        """
        if not exists(self.config_filename):
            raise NoEnvironmentConfigFileError(self.config_filename)

        self._config = tools.load_configuration(self.config_filename, defaults={'root': self.root_path})
        if self._config.has('logging'):
            for d in [ dirname(join(self.root_path, f)) for f in self._config.logging.take(['filename'])['filename']]:
                if not exists(d): makedirs(d)
            logging.config.dictConfig(self._config.logging.as_dict()) 
            self._logger = logging.getLogger('odooenv')
        else:
            self._logger = logging

    def save(self, init=False):
        """
        Save configuration file.
        """
        if not init:
            self._config['Environment.environments'] = ','.join(self.environments) 
        tools.save_configuration(self._config, self.config_filename)

    def update(self, iterate=False, repositories=[]):
        """
        Update sources.

        Arguments:
        iterate -- If true the update the function yield to an iteration.
        """
        for name, repository in self.repositories.iteritems():
            if repository is None:
                raise RuntimeError('Repository %s is not exists' % name)
            if len(repositories) == 0 or name in repositories:
                if repository.state() == 'no exists':
                    command = 'create'
                else:
                    command = 'update'
                if iterate:
                    yield command, repository.local_path, repository.remote_url
                if command == 'create':
                    repository.checkout()
                else:
                    repository.update()

    def create_python_environment(self, name, env):
        """
        Create a new python environment with name
        """
        path = env.dir
        if exists(path): return False
        virtualenv.logger = virtualenv.Logger([(virtualenv.Logger.level_for_integer(2), sys.stdout)])
        virtualenv.create_environment(path,site_packages=False)
        return True

    @property
    def logger(self):
        return self._logger

    @property
    def binary_path(self):
        return join(self.env_path, 'bin')

    @property
    def installables(self):
        bin_path = join(self.root_path, 'bin')
        src_path = self._config.sources.dir
        r = [ Installable(r.method, join(src_path, n), bin_path, logger=self._logger) for n, r in self._config.sources.repos if r.has('method') ]
        return r

    @property
    def modules(self):
        return [ Installable(m, is_application=False) for m in self._config['Environment.modules'].split(',') ]

    def addons(self, token_filter=None, object_filter=None, inherited_filter=None, entity_filter=None):
        config_filename = self.addon_config_filename

        if not token_filter is None:
            filter_re = re.compile(token_filter)
            filter_t = lambda s: filter_re.search(s) != None
        else:
            filter_t = lambda s: True

        if not object_filter is None:
            filter_o = lambda a: object_filter in a.objects[0]
        else:
            filter_o = lambda a: True

        if not inherited_filter is None:
            filter_i = lambda a: inherited_filter in a.objects[1]
        else:
            filter_i = lambda a: True

        if not entity_filter is None:
            filter_e = lambda a: entity_filter in a.entities
        else:
            filter_e = lambda a: True

        for path, ds, fs in walk(self.sources_path, followlinks=True):
            if config_filename in fs and '__init__.py' in fs and filter_t(basename(path)):
                addon = Addon(join(path, config_filename))
                if filter_o(addon) and filter_i(addon) and filter_e(addon):
                    yield addon
                ds = []

    @property
    def addon_config_filename(self):
        if self._config.has('addons') and self._config.addons.has('config'):
            return self._config.addons.config
        else:
            return "__openerp__.py"

    @property
    def version(self):
        return self._config['Environment.version']

    @property
    def repositories(self):
        return dict([ (n, Repository(join(self.sources_path, n), r.url, r.get('branch'))) for n, r in self._config.sources.repos ])

    @property
    def root(self):
        return self._config.get('Environment.root', self.root_path)

    @property
    def sources_path(self):
        return self._config.sources.dir

    @property
    def description_filename(self):
        return self._config['Environment.desc-filename']

    @property
    def reports_path(self):
        return self._config['Environment.reports']

    @property
    def snapshots_path(self):
        if self._config.has('snapshots') and self._config.snapshots.has('dir'):
            return self._config.snapshots.dir
        else:
            return False

    @property
    def addons_dir(self):
        return self._config['Environment.addons']

    @property
    def desc_filename(self):
        return self._config['Environment.desc-filename']

    @property
    def client_config_filename(self):
        return join(self.env_path, 'etc', self._config['Environment.client-config-filename'])

    @property
    def server_config_filename(self):
        if self._config.has('server') and self._config.server.has('config'):
            return self._config.server.config
        else:
            return False

    @property
    def web_config_filename(self):
        if 'Environment.web-config-filename' in self._config:
            return join(self.env_path, 'etc', self._config['Environment.web-config-filename'])
        else:
            False

    @property
    def extracommands(self):
        return self._config.get('Environment.server-extracommands', None)

    @property
    def production(self):
        return self._config.get('Environment.production', False)

    @property
    def language(self):
        return self._config.get('Environment.language', None)

    @property
    def snapshot(self):
        return self._config.get('Database.snapshot', False)

    @property
    def database(self):
        return self._config.get('Database.database', None)

    @property
    def debug(self):
        return self._config.get('Environment.debug', False)

    @property
    def modules_update(self):
        r = self._config.get('Modules.update', '')
        r = [ s for s in r.split(',') if not s == '' ]
        return r

    @property
    def modules_install(self):
        r = self._config.get('Modules.install', '')
        r = [ s for s in r.split(',') if not s == '' ]
        return r

    def execute(self, command, args, no_wait=False, check_for_termination=False):
        """
        Execute a command in the python environment defined in set_python_environment()
        """
        if no_wait:
            P = subprocess.Popen([join(self.root,'bin',command)] + args)
            if check_for_termination:
                time.sleep(5)
                if not P.poll() is None: return None
            return P.pid
        else:
            P = subprocess.Popen([join(self.root,'bin',command)] + args)
            P.wait()
            return None

    def get_tests(self):
        """
        Return dict of tests.
        """
        return self._config.test.as_dict()

    def get_addonsourcepath(self):
        """
        Return a list of path to addons directories.
        """
        if getattr(self, 'addonsourcepath', False):
            return self.addonsourcepath

        python_exe = join(self.root, 'bin', 'python')

        _query_addons = """
import pkg_resources, os.path
print pkg_resources.resource_filename('openerp', 'addons')
"""
       
        p = subprocess.Popen([ python_exe, '-c', _query_addons ],
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=DEVNULL)
        addons_path = p.stdout.readline().strip()
        self.addonsourcepath = addons_path
        return addons_path

def create_environment(path, config_ori):
    """Create environment structure.
    """
    # Archivo de configuracion destino
    config_dst = join(path, 'etc', config_filename)

    if not exists(path) or not listdir(path):
        # Crea el ambiente python
        virtualenv.logger = virtualenv.Logger([(virtualenv.Logger.level_for_integer(2), sys.stdout)])
        virtualenv.create_environment(path,site_packages=False)

        # Crea el directorio donde va el archivo de configuracion
        makedirs(dirname(config_dst))

        # Descarga el archivo de configuracion environment.yml
        urlretrieve(config_ori, config_dst)

    # Prepara el ambiente Odoo
    env = OdooEnvironment(path)
    env.setup()

    return env


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
