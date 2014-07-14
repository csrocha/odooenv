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

import getpass
import pkg_resources
from os.path import join
from tools import Struct, yaml_load
defaults_yml = pkg_resources.resource_stream(__name__, join('data','defaults.yml'))
defaults = yaml_load(defaults_yml)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
