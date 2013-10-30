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

# Use 1 to postgresql v8.x
# Use 3 to postgresql v9.x
default_isolation_level=3

class PostgresNotRunningError(RuntimeError):
    def __init__(self):
        self.message = "No postgresql server to connect.\nPostgreSQL server is not running or other server is locking the database."

def create_database(dbname):
        """
        Create a postgresql database.
        """
        conn = psycopg2.connect("")
        old_isolation_level = conn.isolation_level
        conn.set_isolation_level(0)
        cur = conn.cursor()
        try:
                cur.execute("CREATE DATABASE %s;" % dbname)
        except psycopg2.ProgrammingError:
                cur.execute("DROP DATABASE %s;" % dbname)
                cur.execute("CREATE DATABASE %s;" % dbname)
        conn.set_isolation_level(old_isolation_level)

def drop_database(dbname):
        """
        Drop a postgresql database.
        """
        import psycopg2

        conn = psycopg2.connect("")
        old_isolation_level = conn.isolation_level
        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute("DROP DATABASE %s;" % dbname)
        conn.set_isolation_level(old_isolation_level)

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

def load_configuration(filename, defaults=None):
        """
        Return a dictonary from a ConfigParse format file.
        """
        options = {}
        try:
            p = ConfigParser.ConfigParser(defaults=defaults)
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
            raise RuntimeError('Unable to read config file %s !: %s'% (filename, e))
        return options

def recover_snapshot(dbname, snapshot, oerpenv):
    try:
        #create_database(dbname);
        infile = join(oerpenv.snapshots_path, "%s_%s.dump" % (dbname, snapshot))
        P = subprocess.Popen(['pg_restore', '-x', '-c', '-O', '--disable-triggers', '-Fc', '-d', dbname, infile])
        r = P.wait()
        if r:
            return False
        return True
    except psycopg2.OperationalError:
        raise PostgresNotRunningError

def exists_db(dbname):
    """
    Check if exits a postgresql database.
    """
    try:
        conn = psycopg2.connect("")
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database where datname=%s;", (dbname,))
        return bool(cur.rowcount)
    except:
        raise PostgresNotRunningError


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
