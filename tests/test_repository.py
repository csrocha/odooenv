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

import unittest
import shutil
import os.path

class Test_Repository(unittest.TestCase):
    def test_bazaar_checkout(self):
        from oerpenv.repository import Repository

        self._prepare()

        R = Repository(self._tmpdir, 'lp:openerp')
        R.checkout()

        self._clean()

    def test_bazaar_update(self):
        from oerpenv.repository import Repository

        self._prepare()

        R = Repository(self._tmpdir, 'lp:openerp')
        R.checkout()
        R.update()

        self._clean()

    def test_svn_checkout(self):
        from oerpenv.repository import Repository

        self._prepare()

        R = Repository(self._tmpdir, 'https://dos2unix.svn.sourceforge.net/svnroot/dos2unix')
        R.checkout()

        self._clean()

    def test_svn_update(self):
        from oerpenv.repository import Repository

        self._prepare()

        R = Repository(self._tmpdir, 'https://dos2unix.svn.sourceforge.net/svnroot/dos2unix')
        R.checkout()
        R.update()

        self._clean()

    def _prepare(self):
        self._tmpdir = '/tmp/test'
        if os.path.exists(self._tmpdir): shutil.rmtree(self._tmpdir)

    def _clean(self):
        shutil.rmtree(self._tmpdir)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
