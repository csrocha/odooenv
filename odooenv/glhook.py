# -*- coding: utf-8 -*-
from repository import GITRepository
from werkzeug.wrappers import Request, Response
import json
import re

'''
Documentation:

http://doc.gitlab.com/ee/web_hooks/web_hooks.html

Extensión del versionado según http://semver.org/
   PATCH version sin necesidad de reiniciar el servidor.
         Se actualizan los módulos desde la Interface.
         Hay cambios en las vistas y datos.
   MINOR version con necesidad de reiniciar el servidor.
         Hay cambios en el código fuente.
         Los scripts de actualizacion que se ejecutan son los propios de Odoo.
   MAYOR Hay que reinstalar el Odoo completo en el ambiente.
         Hay cambios en el Odoo ó en la versión de Python.
         Se ejecuta el script de actualización del odooenv?

   PREFIX Indica el prefijo de actualización.
         Se configura en el archivo de configuración del ambiente.

   Archivo de configuración del ambiente:

       glhook:
           port: [Puerto de escucha para el webhook]
           uri: [Git URI del repositorio]
           prefix: [Prefijo del tag a actualizar]

'''

re_tag = re.compile('((?P<prefix>\w+)-)?'
                    'v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')


def tag_split(tag):
    res = re_tag.search(tag)
    if res:
        res = res.groupdict()
        return [res[k] for k in ['prefix', 'major', 'minor', 'patch']]
    else:
        return [False, False, False, False]


class GitLabHook(object):

    def __init__(self, hook, environment):
        self.hook = hook
        self.environment = environment
        self.logger = environment.logger

    def dispatch_request(self, request):
        self.logger.info("New request: %s" % request.headers.items())
        self.logger.debug("Request: %s" % str(request.data))

        if ('Content-Type', 'application/json') not in request.headers.items():
            self.logger.info("Ignore by Format")
            return Response('Ignore by Format')

        data = json.loads(request.data)

        if 'refs/tags/' in data['ref'] and '-' in data['ref']:
            tag = data['ref'].split('/')[-1]
            prefix, major, minor, patch = tag_split(tag)

            if prefix != self.hook.get('prefix', ''):
                self.logger.info("Ignore by prefix")
                return Response('No prefix')

            root_path = self.environment.root_path
            uri = self.hook.get('uri', None)
            branch = self.hook.get('branch', None)

            repo = GITRepository(root_path, uri,
                                 branch=branch, logger=self.logger)
            current_tag = repo.current_tag()

            self.logger.info("Replacing tag %s with %s." % (current_tag, tag))
            repo.update(tag=tag)

            current_prefix, current_major, current_minor, current_patch = \
                tag_split(current_tag)


            if int(current_major) < int(major):
                self.logger.info("Reinstalling.")
                self.environment.stop()
                self.environment.reinstall()
                self.environment.enable_addons()
                self.environment.start()
            elif int(current_minor) < int(minor):
                self.logger.info("Restarting.")
                self.environment.stop()
                self.environment.enable_addons()
                self.environment.start()

            self.logger.info("Update module list in servers.")
            for server in self.environment.servers:
                server.update_module_list()

            self.logger.info("Updated.")
            return Response('Updated')
        else:
            self.logger.info("Ignored by Operation.")
            return Response('Ignored by Operation')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def start(environment):
    from werkzeug.serving import run_simple

    glhook = environment.get_glhooks()

    if not glhook:
        return False

    app = GitLabHook(glhook, environment)
    run_simple(glhook.get('host', '0.0.0.0'), glhook.get('port', 80), app)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
