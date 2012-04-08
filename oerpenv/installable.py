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

from os.path import abspath, basename, dirname, join, exists
import imp
import os
import subprocess
import StringIO

class Installable:
    def __init__(self, method, url, bin_path):
        """
        Init an addon class information 
        """
        self._method = method
        version = None
        repository_type = None
        if exists(url):
            repository_type = 'file'
        if '=' in url and method in ['pip']:
            url, version = url.split('==',1)
        if not repository_type and '+' in url and method in ['pip']:
            repository_type, url = url.split('+',1)
        self._url = url
        self._version = version
        self._repository_type = repository_type
        self._bin_path = bin_path
        self._run = { 'setup': self.run_setup, 'pip': self.run_pip }[method]
        self._name = None
        self._fullname = None
        self._description = None

    def run_setup(self, command):
        bin_path = self._bin_path
        url = self._url
        command = [ join(bin_path, 'python'), join(url,'setup.py'), command ]
        P = subprocess.Popen(command,
                             cwd = url, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = P.stdout.readlines()
        err = P.stderr.readlines()
        r = P.wait()
        return out, err, r

    def run_pip(self, command):
        bin_path = self._bin_path
        url = self._url
        if command in ['install']:
            url = "%s==%s" % (url, self._version) if self._version else url
            url = "%s+%s" % (self._repository_type,url) if not self._repository_type in [None, 'file'] else url
        command = [ join(bin_path, 'pip'), command, url ]
        P = subprocess.Popen(command,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = P.stdout.readlines()
        err = P.stderr.readlines()
        r = P.wait()
        return out, err, r

    def read_description(self):
        """
        Read Installable description.
        """
        method = self._method
        url = self._url

        name = url 
        fullname = 'No fullname'
        description = 'No description'

        if method in ['setup', 'pip'] and self._repository_type in ['file']:
            name, err, r = self.run_setup('--name')
            name=','.join(name).strip() if r == 0 else url 

            fullname, err, r = self.run_setup('--fullname')
            fullname=','.join(fullname).strip() if r == 0 else 'No fullname'

            description, err, r = self.run_setup('--description')
            description=','.join(description).strip() if r == 0 else 'No description'

        elif method in ['pip'] and not self._repository_type in ['hg', 'bzr', 'file']:
            out, err, r = self.run_pip('search')
            try:
                outs = dict([[ j.strip() for j in i.strip().split('- ',1) ] for i in out if '- ' in i ])
            except:
                outs = {}
            if url in outs:
                name = url
                fullname = 'No fullname'
                description = outs[url]
            else:
                print err
                raise RuntimeError('Installable %s not found\nWe found only this options:\n%s' % (url, ''.join(out)))
        elif not self._repository_type in [ 'hg', 'bzr' ]:
            raise RuntimeError('Method not supported or wrong config file.')

        self._name = name
        self._fullname = fullname
        self._description = description

    def install(self):
        out, err, r = self._run('install')

        if (("Successfully installed %s\n" % self.name in out) or
            ("Cleaning up...\n" in out)):
            return True
        else:
            print ''.join(out)
            print '\n'.join(err)

        return False

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        if self._name is None: self.read_description()
        return self._name

    @property
    def fullname(self):
        if self._fullname is None: self.read_description()
        return self._fullname

    @property
    def description(self):
        if self._description is None: self.read_description()
        return ''.join(self._description)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
