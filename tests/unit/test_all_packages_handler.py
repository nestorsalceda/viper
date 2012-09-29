# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing
from hamcrest import *
from pyDoubles.framework import *

import viper
from viper import handlers, mappers, entities

NAME = u'viper'
VERSION = u'0.1'


class TestAllPackagesHandler(testing.AsyncHTTPTestCase):

    def test_index(self):
        when(self.packages.all).then_return([self._package()])

        response = self.fetch(self._url_for())

        assert_that(response.code, is_(httplib.OK))

    def _package(self):
        package = entities.Package(NAME)
        package.store_release(entities.Release(VERSION))

        return package

    def _url_for(self):
        return '/packages'

    def get_app(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))

        return web.Application([
                web.url(r'/packages',
                    handlers.AllPackagesHandler, dict(packages=self.packages),
                    name='packages'
                ),
                web.url(r'/packages/(?P<id_>%s)' % viper.identifier(),
                    handlers.PackageHandler, dict(packages=self.packages, pypi=None, files=None),
                    name='package'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )
