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

from os.path import join
import getpass

config_filename = 'environment.conf'
version = '6.0'
python_environment = 'default'
directory_structure = ['sources', 'reports', 'snapshots']

user = getpass.getuser()

environment_configuration = {
    'Environment.client-config-filename': 'openerp-client.conf',
    'Environment.server-config-filename': 'openerp-server.conf',
    'Environment.sources': '%(root)s/sources',
    'Environment.reports': '%(root)s/reports',
    'Environment.snapshots': '%(root)s/snapshots',
    'Environment.environments': 'default',
}

version_configuration = {
        '5.0': {
            'Environment.version': '5.0',
            'Environment.desc-filename': '__terp__.py',
            'Repositories.server': 'lp:~openerp/openobject-server/5.0',
            'Repositories.client': 'lp:~openerp/openobject-client/5.0',
            'Repositories.addons': 'lp:~openerp/openobject-addons/5.0',
            'Repositories.addons-extra': 'lp:~openerp-commiter/openobject-addons/stable_5.0-extra-addons',
            'Repositories.web': 'lp:~openerp/openobject-client-web/5.0',
        },
        '6.0': {
            'Environment.version': '6.0',
            'Environment.desc-filename': '__openerp__.py',
            'Repositories.server': 'lp:~openerp/openobject-server/6.0',
            'Repositories.client': 'lp:~openerp/openobject-client/6.0',
            'Repositories.addons': 'lp:~openerp/openobject-addons/6.0',
            'Repositories.addons-extra': 'lp:~openerp-commiter/openobject-addons/extra-6.0',
            'Repositories.addons-community': 'lp:~openerp-community/openobject-addons/trunk-addons-community',
            'Repositories.web': 'lp:~openerp/openobject-client-web/6.0',
        }
}

openerp_header = """# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
"""
import os

openerp_footer = "# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:"

options_client_configuration = lambda path: {
    'login.login': 'demo',
    'login.server': 'localhost',
    'login.port': '8070',
    'login.protocol': 'socket://',
    'login.db': 'terp',
    'client.toolbar': 'both',
    'client.theme': 'none',
    'path.share': join(path, 'share', 'openerp-client'),
    'path.pixmaps': join(path, 'share', 'pixmaps', 'openerp-client'),
    'tip.autostart': False,
    'tip.position': 0,
    'form.autosave': False,
    'printer.preview': True,
    'printer.softpath': 'none',
    'printer.softpath_html': 'none',
    'printer.path': 'none',
    'logging.level': 'INFO',
    'logging.output': 'stdout',
    'debug_mode_tooltips':False,
    'client.default_path': os.path.expanduser('~'),
    'support.recipient': 'support@openerp.com',
    'support.support_id' : '',
    'form.toolbar': True,
    'form.submenu': True,
    'client.form_tab': 'top',
    'client.form_tab_orientation': 0,
    'client.lang': False,
    'client.filetype': {},
    'help.index': 'http://doc.openerp.com/',
    'help.context': 'http://doc.openerp.com/v6.0/index.php?model=%(model)s&lang=%(lang)s',
    'client.timeout': 3600,
    'client.form_text_spellcheck': True,
}


addon_description = lambda addon_token: {
    'name': 'Dummy addon %s' % addon_token,
    'version': '0.0',
    'category': 'None',
    'description': 'Dummy addon.',
    'author': user,
    'website': 'http://www.openerp.com/',
    'depends': [],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}

init_body = """
#
# Insert all includes necesary for this module
#

"""

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
