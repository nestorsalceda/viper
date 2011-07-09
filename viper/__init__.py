# -*- coding: utf-8 -*-

import os
from tornado import web
import handlers
import commands

application = web.Application(
    [
        (r'/', handlers.MainHandler),
        (r'/distutils', handlers.DistutilsHandler, dict(distutils_commands=commands.CommandFactory())),
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__), 'templates')
)
