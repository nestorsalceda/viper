# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing
from hamcrest import *
from pyDoubles.framework import *

import viper
from viper import handlers, mappers, entities

FILE = u'viper-0.1.tar.gz'
EGG_FILE = u'viper-0.1.egg'


class TestFileHandler(testing.AsyncHTTPTestCase):

    def test_return_existent_file(self):
        when(self.files.get_by_name).then_return("foo")

        response = self.fetch(self._url_for(FILE))

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', 'application/x-tar'))

    def test_unknown_mime_type_returns_as_binary(self):
        when(self.files.get_by_name).then_return("foo")

        response = self.fetch(self._url_for(EGG_FILE))

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', 'application/octet-stream'))

    def test_non_existent_file_returns_not_found(self):
        when(self.files.get_by_name).then_raise(mappers.NotFoundError())

        response = self.fetch(self._url_for(FILE))

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def _url_for(self, id_):
        return '/files/%s' % id_

    def get_app(self):
        self.files = spy(mappers.FileMapper(None))

        return web.Application([
                web.url(r'/files/(?P<id_>%s)' % viper.identifier(),
                    handlers.FileHandler, dict(files=self.files),
                    name='file'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )
