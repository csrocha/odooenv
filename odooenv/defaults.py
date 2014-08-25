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
from tools import Struct, yaml_load
from os.path import join, exists, expanduser

user_defaults = expanduser(join('~','odooenvrc'))
global_defaults = pkg_resources.resource_stream(__name__, join('data','defaults.yml'))
defaults_yml = open(user_defaults, 'r') if exists(user_defaults) else global_defaults
print "Default file: %s" % defaults_yml.name
defaults = yaml_load(defaults_yml)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
