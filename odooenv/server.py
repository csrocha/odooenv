# -*- coding: utf-8 -*-
import re
import sys
import time
import logging
import logging.config
import oerplib

class OdooServer:
    def __init__(self, name=None, server='localhost', port='8069', user='admin', password='admin'):
        """
        Create an instance of OdooServer class.

        Arguments:
        config_filename -- Full path to the server configuration file.
        """
        self.db = name
        self.host = server
        self.port = port
        self.user = user
        self.password = password
        self.server = None

    def login(self):
        try:
            self.server = oerplib.OERP(
                    server=self.server,
                    protocol='xmlrpc',
                    port=self.port)
            if self.db:
                self.user_id = self.server.login(self.user, self.password, self.db)
            return True
        except:
            return False

    def db_list(self):
        """
        Query for the server database list.
        """
        if self.server:
            self.server = oerplib.OERP(server=self.server, protocol=self.protocol, port=self.port)
            return oerp.db.list()
        else:
            return None

    def update_module_list(self):
        """
        Update module list.
        """
        if self.server:
            mod_obj = self.server.get('ir.module.module')
            mod_obj.update_list()
            return True
        else:
            return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
