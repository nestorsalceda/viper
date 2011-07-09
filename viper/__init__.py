# -*- coding: utf-8 -*-

import os
from tornado import web
import handlers

application = web.Application(
    [
        (r'/', handlers.MainHandler),
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__), 'templates')
)
