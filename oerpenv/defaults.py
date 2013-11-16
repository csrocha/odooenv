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
directory_structure = ['sources', 'reports', 'snapshots', 'etc']

user = getpass.getuser()

environment_configuration = {
    'Environment.client-config-filename': 'openerp-client.conf',
    'Environment.web-config-filename': 'openerp-web.cfg',
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
            'Environment.openerp-web.options': '--server-port=8069 --server-host=localhost --addons=default/addons/ -p 8080',
            'Environment.installables': """
                    pip:bzr+http://download.gna.org/pychart/bzr-archive
                    pip:lxml
                    pip:psycopg2
                    pip:Babel
                    pip:PyYAML
                    pip:reportlab
                    pip:python-dateutil==1.5
                    pip:hg+https://bitbucket.org/johnmc/zkemapi
                    pip:%(sources)s/server
                    setup:%(sources)s/web
            """,
            'Repositories.server': 'lp:~openerp/openobject-server/6.0',
            'Repositories.client': 'lp:~openerp/openobject-client/6.0',
            'Repositories.addons': 'lp:~openerp/openobject-addons/6.0',
            'Repositories.addons-extra': 'lp:~openerp-commiter/openobject-addons/extra-6.0',
            'Repositories.addons-community': 'lp:~openerp-community/openobject-addons/trunk-addons-community',
            'Repositories.web': 'lp:openobject-client-web',
        },
        '6.1': {
            'Environment.version': '6.1',
            'Environment.desc-filename': '__openerp__.py',
            'Environment.installables': """
                    pip:bzr+http://download.gna.org/pychart/bzr-archive
                    pip:lxml
                    pip:psycopg2
                    pip:Babel>=0.9.6
                    pip:simplejson>=2.0.6
                    pip:python-dateutil>=1.4.1,<2
                    pip:python-ldap
                    pip:python-openid
                    pip:werkzeug
                    pip:pywebdav
                    pip:unittest2
                    pip:mock
                    pip:pyyaml
                    pip:reportlab
                    pip:PIL
                    pip:gdata
                    pip:pydot
                    pip:mako
                    pip:psycopg2
                    pip:feedparser
                    pip:zsi
                    pip:pytz
                    pip:vatnumber
                    pip:vobject
                    pip:xlwt
                    pip:pyopenssl
                    pip:PyXML>=0.8.3
                    pip:python-dateutil==1.5
                    pip:hg+https://bitbucket.org/johnmc/zkemapi
                    setup:%(sources)s/server
                    setup:%(sources)s/openerp-web
            """,
            'Repositories.server': 'lp:openobject-server/6.1',
            'Repositories.addons': 'lp:openobject-addons/6.1',
            'Repositories.openerp-web': 'lp:openerp-web/6.1',
        },
        '7.0': {
            'Environment.version': '7.0',
            'Environment.desc-filename': '__openerp__.py',
            'Environment.installables': """
                    pip:bzr+http://download.gna.org/pychart/bzr-archive
                    pip:cython
                    pip:https://github.com/lxml/lxml/archive/lxml-2.3.zip
                    pip:psycopg2
                    pip:Babel
                    pip:PyYAML
                    pip:reportlab
                    pip:PIL
                    pip:python-dateutil==1.5
                    pip:hg+https://bitbucket.org/johnmc/zkemapi
                    setup:%(sources)s/server
            """,
            'Repositories.server': 'lp:openobject-server/7.0',
            'Repositories.addons': 'lp:openobject-addons/7.0',
            'Repositories.openerp-web': 'lp:openerp-web/7.0',
        },
        'trunk': {
            'Environment.version': '8.0',
            'Environment.desc-filename': '__openerp__.py',
            'Environment.installables': """
                    pip:bzr+http://download.gna.org/pychart/bzr-archive
                    pip:cython
                    pip:https://github.com/lxml/lxml/archive/lxml-2.3.zip
                    pip:psycopg2
                    pip:Babel
                    pip:PyYAML
                    pip:reportlab
                    pip:PIL
                    pip:python-dateutil==1.5
                    pip:hg+https://bitbucket.org/johnmc/zkemapi
                    pip:%(sources)s/server
                    pip:%(sources)s/openerp-web
            """,
            'Repositories.server': 'lp:openobject-server/trunk',
            'Repositories.addons': 'lp:openobject-addons/trunk',
            'Repositories.openerp-web': 'lp:openerp-web/trunk',
        },
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

default_files = {
    '%(root)s/etc/openerp-client.conf': """
[printer]
preview = True
softpath_html = None
softpath = None
path = None

[logging]
output = stdout
level = error

[tip]
position = 0
autostart = False

[path]
pixmaps = $(root)s/share/pixmaps/openerp-client
share = $(root)s/share/openerp-client

[client]
form_tab_orientation = 0
form_tab = top
lang = es_AR
theme = None
timeout = 3600
toolbar = both
filetype = {}
#default_path = /home/crocha/Proyectos/openerp/6.0/openerp-argentina/l10n_ar_invoice/i18n
form_text_spellcheck = True

[form]
autosave = False
toolbar = True
submenu = True

[login]
protocol = socket://
login = admin
port = 8070
server = localhost
db = polpor_erp_v6

[support]
support_id = 
recipient = support@openerp.com
""",
    '%(root)s/etc/openerp-server.conf': """
[options]
without_demo = True
; This is the password that allows database operations:
; admin_passwd = admin
upgrade = True
verbose = True
netrpc = True
; netrpc_interface = 
; netrpc_port = 
xmlrpc = True
; xmlrpc_interface = 
xmlrpc_port = 8069
db_host = False
db_port = False
; Please uncomment the following line *after* you have created the
; database. It activates the auto module check on startup.
db_name = ctmil
;db_user = openerp
;db_password = False
; Uncomment these for xml-rpc over SSL
; secure = True
; secure_cert_file = /etc/openerp/server.cert
; secure_pkey_file = /etc/openerp/server.key
root_path = None
soap = False
; translate_modules = ['all']
demo = {}
addons_path = None
reportgz = False

; Static http parameters
static_http_enable = False
static_http_document_root = /var/www/html
static_http_url_prefix = /
""",
    '%(root)s/etc/openerp-client.conf': """
[global]
addons-path=%(root)/addons
"""
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
