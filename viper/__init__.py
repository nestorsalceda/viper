# -*- coding: utf-8 -*-

import os
from tornado import web
import pymongo

from viper import handlers, commands, mappers

def application():
    database = pymongo.Connection()['viper_package_index']

    packages = mappers.PackageMapper(database)
    files = mappers.FileMapper(database)

    submit = commands.SubmitCommand(packages)
    upload = commands.FileUploadCommand(packages, files)

    return web.Application(
        [
            (r'/', handlers.MainHandler),
            (r'/distutils', handlers.DistutilsHandler, dict(submit=submit, upload=upload)),
            web.url(r'/packages/(?P<id_>[a-zA-Z0-9.-]+)',
                handlers.PackageHandler, dict(packages=packages),
                name='package'
            ),
            web.url(r'/packages/(?P<id_>[a-zA-Z0-9.-]+)/(?P<version>[a-zA-Z0-9.-]+)',
                handlers.PackageHandler, dict(packages=packages),
                name='package_with_version'
            )
        ],
        debug=True,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static')
    )
