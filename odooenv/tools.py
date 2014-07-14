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

from os.path import join
import sys, os, ConfigParser
import subprocess
import psycopg2
import select
from logging import DEBUG, ERROR
from yaml import load, safe_load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# convert a dictionary to an structure class
class Struct(object):
    def __init__(self, adict, rdict={}):
        """Convert a dictionary to a class, and format each string
        item using the rdict parameter.

        @param :adict Dictionary
        @rdict :rdict Replacement dictionary.
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v, rdict)
            if isinstance(v, str):
                self.__dict__[k] = v.format(**rdict)

    def as_dict(self):
        """Return a dict from this struct"""
        r = {}
        for k in self.__dict__:
            v = self.__dict__[k]
            r[k] = v.as_dict() if isinstance(v, Struct) else v
        return r

    def take(self, keys):
        r = { k: [] for k in keys }
        for k in self.__dict__:
            v = self.__dict__[k]
            if k in keys:
                r[k].append(v)
            elif isinstance(v, Struct):
                rr = v.take(keys)
                for k in rr:
                    r[k].extend(rr[k])
        return r

    def has(self, key):
        return key in self.__dict__

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
    def __iter__(self):
        for k in self.__dict__:
            yield (k, self.__dict__[k])

# Use 1 to postgresql v8.x
# Use 3 to postgresql v9.x
default_isolation_level=3

def yaml_load(f):
    """
    Load YAML file.
    """
    if not isinstance(f, file) or not isinstance:
        f = open(f)
    return Struct(load(f, Loader=Loader))


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
        with open(filename, 'r') as f:
            config = Struct(safe_load(f), defaults)
            return config
        return False

def load_configuration_old(filename, defaults=None):
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
        conn = psycopg2.connect(database="template1")
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database where datname=%s;", (dbname,))
        return bool(cur.rowcount)
    except:
        raise PostgresNotRunningError

def call(popenargs, logger, stdout_log_level=DEBUG, stderr_log_level=ERROR, **kwargs):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.
    """
    logger.info("Running: " + ' '.join(popenargs))
    child = subprocess.Popen(popenargs, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwargs)
 
    log_level = {child.stdout: stdout_log_level,
                 child.stderr: stderr_log_level}
    output    = {child.stdout: [],
                 child.stderr: []}
 
    def check_io():
        ready_to_read = select.select([child.stdout, child.stderr], [], [], 1000)[0]
        for io in ready_to_read:
            line = io.readline()
            if line:
                output[io].append(line[:-1])
                logger.log(log_level[io], line[:-1])
 
    # keep checking stdout/stderr until the child exits
    while child.poll() is None:
        check_io()
 
    check_io()  # check again to catch anything after the process exits
 
    return output[child.stdout], output[child.stderr], child.wait()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
