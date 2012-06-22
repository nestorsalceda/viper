# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing
from hamcrest import *

from viper import handlers

URL = r'/'


class TestMainHandler(testing.AsyncHTTPTestCase):

    def test_exists_main_page(self):
        response = self.fetch(URL)
        assert_that(response.code, is_(httplib.OK))
        assert_that(response.body, is_not(none()))

    def get_app(self):
        return web.Application([
                (r'/', handlers.MainHandler),
                web.url(r'/packages',
                    handlers.AllPackagesHandler, dict(packages=None),
                    name='packages'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )
