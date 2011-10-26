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

from os.path import abspath, basename, dirname
import imp
import os

class Installable:
    def __init__(self, installable_setup_path):
        """
        Init an addon class information 
        """
        self._installable_setup_path = abspath(installable_setup_path)
        self._path = dirname(self._installable_setup_path)
        self.read_description()

    def read_description(self):
        """
        Read Installable description.
        """
        old_path = os.getcwd()
        os.chdir(self._path)
        sin, sout, serr = os.popen3('python %s --name --fullname --description' % self._installable_setup_path)
        self._name = sout.readline().replace('\n', '')
        self._fullname = sout.readline().replace('\n', '')
        self._description = sout.readlines()
        if self._name == '':
            raise RuntimeError('No description')
        os.chdir(old_path)

    def install(self, python='python'):
        old_path = os.getcwd()
        os.chdir(self._path)
        sin, sout, serr = os.popen3('%s %s install' % (python, self._installable_setup_path))
        print sout.readlines()
        return True

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
