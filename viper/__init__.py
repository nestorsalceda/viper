# -*- coding: utf-8 -*-

import os
from tornado import web
import pymongo

from viper import handlers, commands

def application():
    database = pymongo.Connection()['viper_package_index']
    distutils_commands = commands.CommandFactory(database)

    return web.Application(
        [
            (r'/', handlers.MainHandler),
            (r'/distutils', handlers.DistutilsHandler, dict(distutils_commands=distutils_commands)),
        ],
        debug=True,
        template_path=os.path.join(os.path.dirname(__file__), 'templates')
    )
