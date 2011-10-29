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

from bzrlib.plugin import load_plugins
from bzrlib.branch import Branch
from bzrlib import workingtree
import pysvn

from os.path import abspath, basename, dirname, join
import imp
import os
import re
import subprocess
import StringIO

class RepositoryBase:
    def __init__(self, local_path, remote_url):
        self.local_path = local_path
        self.remote_url = remote_url

    def update(self):
        raise NotImplementedError

    def checkout(self):
        raise NotImplementedError

    _url_re_ = []

class BazaarRepository(RepositoryBase):
    def __init__(self, local_path, remote_url):
        self = RepositoryBase.__init__(self, local_path, remote_url)
        load_plugins()

    def update(self):
        from bzrlib import workingtree
        wt = workingtree.WorkingTree.open(self.local_path)
        wt.update()

    def checkout(self):
        remote_branch = Branch.open(self.remote_url)
        local_branch = remote_branch.bzrdir.sprout(
                self.local_path).open_branch()

    _url_re_ = [
        re.compile('^lp:.*$'),
        re.compile('bzr+ssh:.*')
    ]

class SVNRepository(RepositoryBase):
    def __init__(self, local_path, remote_url):
        self = RepositoryBase.__init__(self, local_path, remote_url)
        load_plugins()

    def update(self):
        client = pysvn.Client()
        client.update(self.local_path)

    def checkout(self):
        client = pysvn.Client()
        client.checkout(self.remote_url, self.local_path)

    _url_re_ = [
        re.compile('^https:.*$'),
        re.compile('^svn:.*$'),
        re.compile('^svn+ssh:.*'),
    ]


def Repository(local_path, branch_url):
    classes = [ BazaarRepository, SVNRepository ]
    for c in classes:
        if any([ ure.search(branch_url) is not None for ure in c._url_re_ ]):
            return c(local_path, branch_url)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
 
