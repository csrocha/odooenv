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
import sys, os, ConfigParser
import subprocess
import psycopg2

def create_database(dbname):
        """
        Create a postgresql database.
        """
        conn = psycopg2.connect("")
        conn.set_isolation_level(0)
        cur = conn.cursor()
        try:
                cur.execute("CREATE DATABASE %s;" % dbname)
        except psycopg2.ProgrammingError:
                cur.execute("DROP DATABASE %s;" % dbname)
                cur.execute("CREATE DATABASE %s;" % dbname)
        conn.set_isolation_level(3)

def drop_database(dbname):
        """
        Drop a postgresql database.
        """
        import psycopg2

        conn = psycopg2.connect("")
        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute("DROP DATABASE %s;" % dbname)
        conn.set_isolation_level(3)

def save_configuration(options, filename):
        """
        Save a configuration file with options dict data.
        """
        try:
            p = ConfigParser.ConfigParser()
            sections = {}
            for o in options.keys():
                if not len(o.split('.'))==2:
                    continue
                osection,oname = o.split('.')
                if not p.has_section(osection) and osection != 'DEFAULT':
                    p.add_section(osection)
                p.set(osection,oname,options[o])
            p.write(file(filename,'wb'))
        except:
            print 'Unable to write config file %s !'% (filename,)
        return True

def load_configuration(filename):
        """
        Return a dictonary from a ConfigParse format file.
        """
        options = {}
        try:
            p = ConfigParser.ConfigParser()
            p.read([filename])
            for section in p.sections():
                for (name,value) in p.items(section):
                    if value=='True' or value=='true':
                        value = True
                    if value=='False' or value=='false':
                        value = False
                    if value=='None' or value=='none':
                        value = None
                    options[section+'.'+name] = value
        except Exception, e:
            print 'Unable to read config file %s !'% filename
        return options

def recover_snapshot(dbname, snapshot, oerpenv):
    create_database(dbname);
    infile = join(oerpenv.snapshots_path, "%s_%s.dump" % (dbname, snapshot))
    P = subprocess.Popen(['pg_restore', '-Fc', '-d', dbname, infile])
    r = P.wait()
    if r:
        return False
    return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
