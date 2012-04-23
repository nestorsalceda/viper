# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing
from hamcrest import *
from pyDoubles.framework import *

from viper import handlers, mappers, entities

NAME = u'viper'
VERSION = u'0.1'


class TestPackageHandler(testing.AsyncHTTPTestCase):

    def test_show_existent_package(self):
        when(self.packages.get_by_name).then_return(self._package())

        response = self.fetch(self._url_for(NAME))

        assert_that(response.code, is_(httplib.OK))

    def _package(self):
        package = entities.Package(NAME)
        package.store_release(entities.Release(VERSION))

        return package

    def test_non_existent_package_returns_not_found(self):
        when(self.packages.get_by_name).then_raise(mappers.NotFoundError())

        response = self.fetch(self._url_for(NAME))

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def _url_for(self, id_):
        return '/packages/%s' % id_

    def get_app(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))

        return web.Application([
                (r'/packages/(?P<id_>[a-zA-Z0-9]+)', handlers.PackageHandler, dict(packages=self.packages))
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )
