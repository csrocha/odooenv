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
from os.path import abspath, basename, dirname, join, exists
import imp
import os
import re
import subprocess
import StringIO

try:
    import pysvn
    without_svn = False
except:
    without_svn = True

class RepositoryBase:
    def __init__(self, local_path, remote_url, branch=None):
        self.local_path = local_path
        self.remote_url = remote_url
        self.branch = branch

    def update(self):
        raise NotImplementedError

    def checkout(self):
        raise NotImplementedError

    def state(self):
        if exists(self.local_path):
            return 'exists'
        else:
            return 'no exists'

    _url_re_ = []

class BazaarRepository(RepositoryBase):
    def __init__(self, local_path, remote_url, branch=None):
        self = RepositoryBase.__init__(self, local_path, remote_url, branch=branch)
        load_plugins()

    def update(self):
        from bzrlib import workingtree
        wt = workingtree.WorkingTree.open(self.local_path)
        wt.update()
        #remote_branch = Branch.open(self.remote_url)
        #wt.pull(remote_branch)

    def checkout(self):
        #import pdb; pdb.set_trace()
        remote_branch = Branch.open(self.remote_url)
        tree = remote_branch.create_checkout(self.local_path, lightweight=True)
        #local_branch = remote_branch.bzrdir.sprout(
        #        self.local_path).open_branch()

    _url_re_ = [
        re.compile('^lp:.*$'),
        re.compile('^bzr+ssh:.*')
    ]

def ssl_server_trust_prompt( trust_dict ):
    # http://pysvn.tigris.org/docs/pysvn_prog_ref.html#pysvn_client_callback_ssl_server_trust_prompt
    for v in trust_dict.items():
       print "%s:%s" % v
    a = raw_input("Your trust in the certificate? ")
    return a in 'Yesyes', trust_dict['failures'], True

class SVNRepository(RepositoryBase):
    def __init__(self, local_path, remote_url, branch=None):
        if without_svn:
            raise RuntimeError("You need install PySVN to use SVN capabilities.")

        self = RepositoryBase.__init__(self, local_path, remote_url,branch=branch)
        load_plugins()

    def update(self):
        client = pysvn.Client()
        client.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
        client.update(self.local_path)

    def checkout(self):
        client = pysvn.Client()
        client.callback_ssl_server_trust_prompt = ssl_server_trust_prompt
        client.checkout(self.remote_url, self.local_path)

    _url_re_ = [
        re.compile('^https:.*(?<!\.git)$'),
        re.compile('^svn:.*$'),
        re.compile('^svn+ssh:.*'),
    ]

class GITRepository(RepositoryBase):
    def __init__(self, local_path, remote_url, branch=None):
        self = RepositoryBase.__init__(self, local_path, remote_url, branch=branch)

    def update(self):
        olddir = os.getcwd()
        os.chdir(self.local_path)
        subprocess.call(['git', 'pull'])
        os.chdir(olddir)

    def checkout(self):
        git_command = ['git', 'clone']
        git_command.extend(['--depth', '1', '--single-branch'])
        if self.branch:
            git_command.extend(['--branch', str(self.branch)])
        git_command.extend([self.remote_url, self.local_path])
        subprocess.call(git_command)

    _url_re_ = [
        re.compile('^https:.*\.git$'),
        re.compile('^git@.*$'),
    ]

def Repository(local_path, branch_url, branch=None):
    classes = [ BazaarRepository, SVNRepository, GITRepository ]
    for c in classes:
        if any([ ure.search(branch_url) is not None for ure in c._url_re_ ]):
            return c(local_path, branch_url, branch=branch)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
 
