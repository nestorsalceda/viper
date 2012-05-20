# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing

from pyDoubles.framework import *
from hamcrest import *

import viper
from viper import handlers, mappers, entities

NAME = u'viper'
VERSION = u'0.1dev'
FILENAME = u'viper-0.1dev.tar.gz'
ROOT_URL = r'/distutils/'
PACKAGE_URL = u'/distutils/%s/' % NAME


class TestDistutilsDownloadHandler(testing.AsyncHTTPTestCase):

    def test_generate_simple_html_interface_for_all_packages(self):
        when(self.packages.all).then_return(iter([entities.Package(NAME)]))

        response = self.fetch(ROOT_URL)

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', contains_string('text/html')))

        assert_that(response.body, contains_string('<a href="/distutils/viper/" title="viper">viper</a>'))

    def test_generate_simple_html_interface_for_all_packages_without_any_package(self):
        when(self.packages.all).then_return(iter([]))

        response = self.fetch(ROOT_URL)

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', contains_string('text/html')))

        assert_that(response.body, contains_string('<body>\n\n</body>'))

    def test_generate_simple_html_interface_for_a_package(self):
        when(self.packages.get_by_name).then_return(self._package())

        response = self.fetch(PACKAGE_URL)

        assert_that(response.code, is_(httplib.OK))
        assert_that(response.headers, has_entry('Content-Type', contains_string('text/html')))

        assert_that(response.body, all_of(
            contains_string('<h1>Links for viper</h1>'),
            contains_string('<a href="/files/%s">%s</a>' % (FILENAME, FILENAME))
        ))

    def _package(self):
        package = entities.Package(NAME)
        release = entities.Release(VERSION)
        release.add_file(entities.File(FILENAME, None, None))
        package.store_release(release)

        return package

    def test_redirect_to_fallback_if_not_exists(self):
        when(self.packages.get_by_name).then_raise(mappers.NotFoundError)

        response = self.fetch(PACKAGE_URL, follow_redirects=False)

        assert_that(response.code, is_(httplib.FOUND))
        assert_that(response.headers, has_entry('Location', self.pypi_fallback % NAME))

    def get_app(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))
        self.pypi_fallback = "http://pypi.python.org/simple/%s/"

        return web.Application([
                web.url(r'/distutils/',
                    handlers.DistutilsDownloadHandler, dict(packages=self.packages)
                ),
                web.url(r'/distutils/(?P<id_>%s)/' % viper.identifier(),
                    handlers.DistutilsDownloadHandler, dict(packages=self.packages),
                    name='distutils_package'
                ),
                web.url(r'/packages/(?P<id_>%s)' % viper.identifier(),
                    handlers.PackageHandler, dict(packages=self.packages, pypi=None, files=None),
                    name='package'
                ),
                web.url(r'/files/(?P<id_>%s)' % viper.identifier(),
                    handlers.FileHandler, dict(files=None),
                    name='file'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static'),
            pypi_fallback=self.pypi_fallback
        )
