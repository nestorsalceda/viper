# -*- coding: utf-8 -*-

import os
from tornado import web
import pymongo

import handlers
import commands

database = pymongo.Connection()['viper_package_index']

application = web.Application(
    [
        (r'/', handlers.MainHandler),
        (r'/distutils', handlers.DistutilsHandler, dict(distutils_commands=commands.CommandFactory(database))),
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__), 'templates')
)
