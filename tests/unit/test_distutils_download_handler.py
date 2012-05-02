# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing

from pyDoubles.framework import *
from hamcrest import *

import viper
from viper import handlers, mappers, entities

URL = r'/distutils/'
NAME = u'viper'


class TestDistutilsDownloadForAllPackagesHandler(testing.AsyncHTTPTestCase):

    def test_generate_simple_html_interface(self):
        when(self.packages.all).then_return(iter([entities.Package(NAME)]))

        response = self.fetch(URL)

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', contains_string('text/html')))

        assert_that(response.body, contains_string('<a href="/distutils/viper/" title="viper">viper</a>'))

    def test_generate_simple_html_interface_without_any_package(self):
        when(self.packages.all).then_return(iter([]))

        response = self.fetch(URL)

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', contains_string('text/html')))

        assert_that(response.body, contains_string('<body>\n\n</body>'))

    def get_app(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))

        return web.Application([
                web.url(r'/distutils/',
                    handlers.DistutilsDownloadHandler, dict(packages=self.packages)
                    ),
                web.url(r'/distutils/(?P<id_>%s)/' % viper.identifier(),
                    handlers.DistutilsDownloadHandler, dict(packages=self.packages),
                    name='distutils_package'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )
