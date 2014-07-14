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
import re
import subprocess
import StringIO
import logging
from tools import call

class Installable:
    def __init__(self, method, url, bin_path, logger=logging):
        """
        Init an addon class information 
        """
        self._method = method
        repository_type = None
        if exists(url):
            repository_type = 'file'
        elif '+' in url and method in ['pip']:
            repository_type, url = url.split('+',1)
        elif not '+' in url and ':' in url and method in ['pip']:
            repository_type = url.split(':',1)[0]
        self._url = url
        self._repository_type = repository_type
        self._bin_path = bin_path
        self._run = { 'setup': self.run_setup, 'pip': self.run_pip }[method]
        self._short_name = re.split(r'[<>=]+', url, 1)[0]
        self._name = None
        self._fullname = None
        self._description = None
        self._logger=logger

    def run_setup(self, command):
        bin_path = self._bin_path
        url = self._url
        command = [ join(bin_path, 'python'), join(url,'setup.py'), command ]
        return call(command, self._logger, cwd=url)

    def run_pip(self, command):
        bin_path = self._bin_path
        url = self._url
        if command in ['install']:
            url = "%s+%s" % (self._repository_type,url) if not self._repository_type in [None, 'file', 'http', 'https'] else url
        if command in ['search']:
            url = self._short_name
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
            if r != 0:
                print "ERROR: This package is not well configured, or you need install previous modules to make it work"
                print err
            name=','.join(name).strip() if r == 0 else url 

            fullname, err, r = self.run_setup('--fullname')
            fullname=','.join(fullname).strip() if r == 0 else 'No fullname'

            description, err, r = self.run_setup('--description')
            description=','.join(description).strip() if r == 0 else 'No description'

        elif method in ['pip'] and not self._repository_type in ['hg', 'bzr', 'file', 'http', 'https']:
            out, err, r = self.run_pip('search')
            try:
                outs = dict([
                    (lambda(a,b): (a.strip().lower(), b))(re.split(r'\s*-\s+',i,1))
                    for i in out if '- ' in i ])
            except:
                outs = {}
            if self._short_name.lower() in outs:
                name = self._short_name
                fullname = 'No fullname'
                description = outs[self._short_name.lower()]
            else:
                raise RuntimeError('Installable %s not found\nWe found only this options:\n%s' % (url, ''.join(out)))
        elif not self._repository_type in [ 'hg', 'bzr', 'http', 'https' ]:
            raise RuntimeError('Method not supported or wrong config file.')

        self._name = name
        self._fullname = fullname
        self._description = description

    def install(self):
        out, err, r = self._run('install')

        if (r == 0):
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
