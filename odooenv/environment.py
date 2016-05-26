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
import signal
import time
from time import sleep
import logging
import logging.config
from os import makedirs, walk, listdir, kill
from os.path import abspath, join, exists, dirname, basename, realpath, lexists
from installable import Installable
from odooenv import tools
from virtualenv import subprocess
from addon import Addon
from repository import Repository
from urllib import urlretrieve
from server import OdooServer
import ConfigParser

try:
    from subprocess import DEVNULL
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
        for d in [join(self.root_path, d)
                  for d in self._config.take(['dir'])['dir']]:
            if not exists(d):
                makedirs(d)

    def load(self):
        """
        Load configuration file.
        """
        if not exists(self.config_filename):
            raise NoEnvironmentConfigFileError(self.config_filename)

        self._config = tools.load_configuration(
            self.config_filename, defaults={'root': self.root_path})
        if self._config.has('logging'):
            for d in [
                dirname(join(self.root_path, f))
                for f in self._config.logging.take(['filename'])['filename']
            ]:
                if not exists(d):
                    makedirs(d)
            logging.config.dictConfig(self._config.logging.as_dict())
            self._logger = logging.getLogger('odooenv')
        else:
            self._logger = logging

    def save(self, init=False):
        """
        Save configuration file.
        """
        if not init:
            self._config['Environment.environments'] = (
                ','.join(self.environments))
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

    def reset_python_environment(self):
        """
        Reset the python environment.
        """
        path = self.root_path
        if not exists(path):
            return False
        virtualenv.logger = virtualenv.Logger(
            [(virtualenv.Logger.level_for_integer(2), sys.stdout)])
        virtualenv.create_environment(path, site_packages=False)
        return True

    @property
    def logger(self):
        return self._logger

    @property
    def installables(self):
        bin_path = join(self.root_path, 'bin')
        src_path = self._config.sources.dir
        r = [Installable(r.method, join(src_path, n),
                         bin_path, logger=self._logger)
             for n, r in self._config.sources.repos if r.has('method')]
        return r

    @property
    def modules(self):
        return [Installable(m, is_application=False)
                for m in self._config['Environment.modules'].split(',')]

    def addons(self, token_filter=None, model_filter=None,
               inherited_filter=None, data_filter=None,
               field_filter=None):
        config_filename = self.addon_config_filename
        addonsourcepath = self.get_addonsourcepath()

        filter_re = re.compile(token_filter) if token_filter else None

        def filter_name(p):
            return filter_re.search(p) is not None if token_filter else True

        def filter_addon(a):
            return (
                (model_filter in a.models[0] if model_filter else True)
                and (data_filter in a.data if data_filter else True)
                and (inherited_filter in a.models[1]
                     if inherited_filter else True)
                and (field_filter in [f for fn, cl, f in a.fields]
                     if field_filter else True)
            )

        for path, ds, fs in walk(self.sources_path, followlinks=True):
            if (
                config_filename in fs and
                '__init__.py' in fs and
                filter_name(basename(path)) and
                realpath(path) != realpath(addonsourcepath)
            ):
                addon = Addon(join(path, config_filename))
                if (filter_addon(addon)):
                    yield addon

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
        return {n: Repository(join(self.sources_path, n),
                              r.url,
                              r.get('branch'),
                              getattr(r, 'shallow', False))
                for n, r in self._config.sources.repos}

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
        return join(
            self.env_path,
            'etc',
            self._config['Environment.client-config-filename'])

    @property
    def server_config_filename(self):
        if self._config.has('server') and self._config.server.has('config'):
            return self._config.server.config
        else:
            return False

    @property
    def web_config_filename(self):
        if 'Environment.web-config-filename' in self._config:
            return join(
                self.env_path,
                'etc',
                self._config['Environment.web-config-filename'])
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
        r = [s for s in r.split(',') if not s == '']
        return r

    @property
    def modules_install(self):
        r = self._config.get('Modules.install', '')
        r = [s for s in r.split(',') if not s == '']
        return r

    @property
    def server_config(self):
        cfg = self.server_config_filename
        cp = ConfigParser.ConfigParser()
        try:
            cp.readfp(open(cfg))
        except:
            return False

        return cp

    @property
    def servers(self):
        cp = self.server_config

        server = cp.get('options', 'xmlrpc_interface') or 'localhost'
        port = cp.get('options', 'xmlrpc_port') or '8069'

        for tag, db in self._config.get('databases', []):
            if hasattr(db, 'name') and \
                    hasattr(db, 'user') and \
                    hasattr(db, 'password'):
                yield OdooServer(
                    db.name,
                    server,
                    port,
                    db.user,
                    db.password)
            else:
                print "Can't connect to server %s."\
                    " Incomplete section 'databases'."\
                    " Needs name, user & password for each database."\
                    % (db.name,)

    def execute(self, command, args, no_wait=False,
                check_for_termination=False):
        """
        Execute a command in the python environment defined in
        set_python_environment()
        """
        if no_wait:
            P = subprocess.Popen([join(self.root, 'bin', command)] + args)
            if check_for_termination:
                time.sleep(5)
                if not P.poll() is None:
                    return None
            return P.pid
        else:
            P = subprocess.Popen([join(self.root, 'bin', command)] + args)
            P.wait()
            return None

    def get_tests(self):
        """
        Return dict of tests.
        """
        if self._config.has('test'):
            return self._config.test.as_dict()
        else:
            return []

    def get_glhooks(self):
        """
        Return dict of GitLab Webhooks.
        """
        if self._config.has('glhook'):
            return self._config.glhook.as_dict()
        else:
            return False

    def get_addonsourcepath(self):
        """
        Return a list of path to addons directories.
        """
        if getattr(self, 'addonsourcepath', False):
            return self.addonsourcepath

        if self.server_config and self.server_config.has_option('options',
                                                                'addons_path'):
            paths = self.server_config.get('options', 'addons_path')
            for p in paths.split(','):
                p = os.path.abspath(p)
                if exists(p) and os.access(p, os.W_OK):
                    addons_path = p
                else:
                    return False
        else:

            python_exe = join(self.root, 'bin', 'python')

            _query_addons = """
            import pkg_resources, os.path
            print pkg_resources.resource_filename('openerp', 'addons')
            """
            p = subprocess.Popen(
                [python_exe, '-c', _query_addons], stdout=subprocess.PIPE,
                stdin=subprocess.PIPE, stderr=DEVNULL)
            addons_path = p.stdout.readline().strip() or False

        self.addonsourcepath = addons_path
        return addons_path

    def start(self,
              database=None,
              snapshot=None,
              debug=False,
              production=True,
              extracommands=None):
        options = []

        if not lexists(self.server_config_filename):
            options += ['--save']
            addons_path = self.get_addonsourcepath()
            options += ['--addons-path', addons_path] if addons_path else []

        if database and database is not None:
            options += ['-d', database]

        if self.server_config_filename:
            options += ['--config', self.server_config_filename]

        if debug:
            options += ['--debug']

        if production:
            options += ['--without-demo=all']

        if extracommands is not None:
            options += extracommands

        if snapshot:
            if database is None:
                print "ERROR: Cant recover snapshot %s," \
                    "because no database defined." % snapshot
                return -1
            print "Recovering snapshot '%s' of the database '%s'." % \
                (snapshot, database)
            if not tools.recover_snapshot(database, snapshot, self):
                print "ERROR: Cant recover snapshot %s." % snapshot
                return False

        # Setup pid file
        pid_filename = join(self.root_path, 'var', 'server.pid')
        if not lexists(dirname(pid_filename)):
            makedirs(dirname(pid_filename))
        options += ['--pidfile', pid_filename]

        try:
            if lexists(pid_filename):
                pid = int(''.join(open(pid_filename).readlines()))
                kill(pid, 0)
                print "A server is running or .server_pid has not been deleted" \
                    " at the end of the server."
                print "Execute 'odooenv stop' to stop the server and" \
                    " remove this file."
                return False
            print "Running with options: %s" % ' '.join(options)
            self.execute('odoo.py', options, no_wait=not debug)
        except KeyboardInterrupt:
            print "KeyboardInterrupt event."
        except OSError, m:
            import sys
            import traceback
            print "Environment Error."
            print "ERROR: %s" % m
            traceback.print_exc(file=sys.stdout)
            print "If you move the environment please rebuild default" \
                " python environment and check directories in"\
                " environment.yml file."
            print "If all ok, be sure you executed 'odooenv install'" \
                " before run this command."
            return False
        return True

    def stop(self):
        pid_filename = join(self.root_path, 'var', 'server.pid')
        if lexists(pid_filename):
            try:
                with open(pid_filename, 'r') as f:
                    pid = int(f.readline())
                os.kill(pid, signal.SIGTERM if True else signal.SIGKILL)
                sleep(3)
                return 0
            except OSError:
                print "No server running."
                return -1
            finally:
                if lexists(pid_filename):
                    os.remove(pid_filename)
        else:
            print "No pid information."
            return False

    def reinstall(self):
        home_dir, lib_dir, inc_dir, bin_dir = virtualenv.path_locations(
            self.root_path)
        virtualenv.install_python(home_dir, lib_dir, inc_dir, bin_dir,
                                  False, True)
        self.install()

    def install(self, developer_mode=False):
        for app in self.installables:
            print "Installing %s%s" % (app.name,
                                       ' as developer'
                                       if developer_mode else '')
            if app.install(developer_mode):
                print "Successfull installed"
            else:
                print "ERROR:"\
                    " Can't confirm the application or module is installed.\n"\
                    "Please, execute 'odooenv test base' to check if server is"\
                    " working.\n"\
                    "To check if client is working execute 'odoo client'.\n"\
                    "If not working,"\
                    " recreate the python environment and try again."

    def server_installed(self):
        logger = self.logger
        try:
            addons_path = self.get_addonsourcepath()
        except:
            if addons_path == "":
                logger.error("Server is not installed")
            return False

        if not addons_path:
            logger.error("Install the server. If not try the following:")
            logger.error(
                "Check if PYTHON_EGG_CACHE if set in writeable directory.\n"
                "Your can use:\nexport PYTHON_EGG_CACHE=%s/.python-eggs" %
                self.root)
            return False

        if not lexists(addons_path):
            logger.error("Execute 'odooenv install' before 'odooenv enable'")
            return False

        return True

    def enable_addons(self, addons=None, ignore_depends=False):
        logger = self._logger

        if not self.server_installed():
            logger.error("Server is not installed.")
            return False

        if isinstance(addons, set):
            addons = {a.token: a for a in self.addons() if a.token in addons}

        if addons is None:
            addons = dict([(addon.token, addon) for addon in self.addons()])
        addons_set = set(addons.keys())

        to_install = addons_set
        yet_enabled = set()
        who_install = {}
        c = 0
        c_t = len(to_install)

        while to_install:
            addon_name = to_install.pop()

            # Ignore base addon
            if addon_name == 'base':
                continue

            # Ignore modules not available.
            if addon_name in addons:
                addon = addons[addon_name]
            else:
                logger.error("ERROR: %s try to install %s, but is unavailable."
                             % (who_install[addon_name], addon_name))
                continue

            for item in set(addon.depends):
                who_install[item] = addon_name

            if not ignore_depends:
                to_install.update(addon.depends)

            if addon.is_enable(self):
                logger.info("Updating %s (%i:%s)" %
                            (addon_name, len(to_install), addon.path))
            else:
                logger.info("Installing %s (%i:%s)" %
                            (addon_name, len(to_install), addon.path))

            yet_enabled.add(addon_name)
            to_install = to_install - yet_enabled
            addon.enable(self, force=True)
            addon.install_externals(self)

            c = c + 1

        return (c_t - c)


def create_environment(path, config_ori):
    """Create environment structure.
    """
    # Archivo de configuracion destino
    config_dst = join(path, 'etc', config_filename)

    if not exists(path) or not listdir(path):
        # Crea el ambiente python
        virtualenv.logger = virtualenv.Logger(
            [(virtualenv.Logger.level_for_integer(2), sys.stdout)])
        virtualenv.create_environment(path, site_packages=False)

        # Crea el directorio donde va el archivo de configuracion
        makedirs(dirname(config_dst))

        # Descarga el archivo de configuracion environment.yml
        urlretrieve(config_ori, config_dst)

    # Prepara el ambiente Odoo
    env = OdooEnvironment(path)
    env.setup()

    return env


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
