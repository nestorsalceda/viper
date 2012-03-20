# -*- coding: utf-8 -*-

import httplib

from tornado.testing import AsyncHTTPTestCase
from hamcrest import *

from viper import application

URL = r'/'


class TestMainHandler(AsyncHTTPTestCase):

    def test_exists_main_page(self):
        response = self.fetch(URL)
        assert_that(response.code, is_(httplib.OK))
        assert_that(response.body, is_not(none()))

    def get_app(self):
        return application
