# -*- coding: utf-8 -*-
import oerplib


class OdooServer:
    def __init__(self, name=None, server='localhost',
                 port='8069', user='admin', password='admin'):
        """
        Create an instance of OdooServer class.

        Arguments:
        config_filename -- Full path to the server configuration file.
        """
        self.server = oerplib.OERP(server=server, protocol='xmlrpc', port=port)
        if name:
            self.user = self.server.login(user, password, name)

    def db_list(self):
        """
        Query for the server database list.
        """
        self.server = oerplib.OERP(server=self.server,
                                   protocol=self.protocol, port=self.port)
        return self.server.db.list()

    def update_module_list(self):
        """
        Update module list.
        """
        mod_obj = self.server.get('ir.module.module')
        mod_obj.update_list()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
