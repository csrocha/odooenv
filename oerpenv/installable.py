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
import imp
import os
import subprocess
import StringIO

class Installable:
    def __init__(self, installable_setup_path):
        """
        Init an addon class information 
        """
        self._installable_setup_path = abspath(installable_setup_path)
        self._path = dirname(self._installable_setup_path)
        self.read_description()

    def run_setup(self, command, bin_path=''):
        command = [ join(bin_path, 'python'), join(self._path,'setup.py'), command ]
        P = subprocess.Popen(command,
                            cwd = self._path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = P.stdout.readlines()
        err = P.stderr.readlines()
        r = P.wait()
        return out, err, r

    def read_description(self):
        """
        Read Installable description.
        """
        name, err, r = self.run_setup('--name')
        if not r == 0:
            raise RuntimeError('No description')
        fullname, err, r = self.run_setup('--fullname')
        if not r == 0:
            raise RuntimeError('No description')
        description, err, r = self.run_setup('--description')
        if not r == 0:
            raise RuntimeError('No description')
        self._name = ','.join(name)[:-1]
        self._fullname = ','.join(fullname)[:-1]
        self._description = ''.join(description)[:-1]

    def install(self, bin_path='', methods=['pip', 'setup.py']):
        for method in methods:
            if method in ['setup.py', 'python']:
                command = [ join(bin_path, 'python'), join(self._path,'setup.py'), 'install' ]
            elif method in ['pip', 'easy_install']:
                command = [ join(bin_path, method), 'install', self._path ]
            else:
                return False
            P = subprocess.Popen(command, cwd=self._path,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = P.stdout.readlines()
            err = P.stderr.readlines()
            r = P.wait()
            if "Successfully installed %s\n" % self._name in out:
                return True
        return False

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def fullname(self):
        return self._fullname

    @property
    def description(self):
        return ''.join(self._description)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
