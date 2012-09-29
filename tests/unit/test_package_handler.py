# -*- coding: utf-8 -*-

import os
import httplib

from tornado import web, testing
from hamcrest import *
from pyDoubles.framework import *

import viper
from viper import handlers, mappers, entities, cache, errors

NAME = u'viper'
VERSION = u'0.1'
INEXISTENT_VERSION = u'0.2'


class TestPackageHandlerToLastVersion(testing.AsyncHTTPTestCase):

    def test_show_existent_package(self):
        when(self.packages.get_by_name).then_return(self._package())

        response = self.fetch(self._url_for(NAME))

        assert_that(response.code, is_(httplib.OK))

    def _package(self):
        package = entities.Package(NAME)
        package.store_release(entities.Release(VERSION))

        return package

    def test_non_existent_package_returns_not_found(self):
        when(self.packages.get_by_name).then_raise(errors.NotFoundError())

        response = self.fetch(self._url_for(NAME))

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def test_cache_a_package_from_pypi(self):
        response = self.fetch(self._url_for(NAME), method='POST', body='')

        assert_that(response.code, is_(httplib.CREATED))
        assert_that(response.headers, has_entry('Location', '/packages/%s' % NAME))
        assert_that_method(self.cache.cache_package).was_called()

    def test_cache_a_non_existing_package_from_pypi_returns_not_found(self):
        when(self.cache.cache_package).then_raise(errors.NotFoundError())

        response = self.fetch(self._url_for(NAME), method='POST', body='')

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def test_cache_a_package_from_pypi_returns_conflict_if_already_exists(self):
        when(self.cache.cache_package).then_raise(errors.AlreadyExistsError)

        response = self.fetch(self._url_for(NAME), method='POST', body='')

        assert_that(response.code, is_(httplib.CONFLICT))

    def _url_for(self, id_):
        return '/packages/%s' % id_

    def get_app(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))
        self.cache = spy(cache.Cache(self.packages, None, None))

        return web.Application([
                web.url(r'/packages/(?P<id_>%s)' % viper.identifier(),
                    handlers.PackageHandler, dict(packages=self.packages, cache=self.cache),
                    name='package'
                ),
                web.url(r'/packages/(?P<id_>%s)/(?P<version>%s)' % (viper.identifier(), viper.identifier()),
                    handlers.PackageHandler, dict(packages=self.packages, cache=self.cache),
                    name='package_with_version'
                ),
                web.url(r'/packages',
                    handlers.AllPackagesHandler, dict(packages=None),
                    name='packages'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )


class TestPackageHandlerWithSpecifiedVersion(testing.AsyncHTTPTestCase):

    def test_show_existent_package_and_version(self):
        when(self.packages.get_by_name).then_return(self._package())

        response = self.fetch(self._url_for(NAME, VERSION))

        assert_that(response.code, is_(httplib.OK))

    def _package(self):
        package = entities.Package(NAME)
        package.store_release(entities.Release(VERSION))

        return package

    def test_non_existent_package_returns_not_found(self):
        when(self.packages.get_by_name).then_raise(errors.NotFoundError())

        response = self.fetch(self._url_for(NAME, VERSION))

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def test_package_without_version_specified_returns_not_found(self):
        when(self.packages.get_by_name).then_return(self._package())

        response = self.fetch(self._url_for(NAME, INEXISTENT_VERSION))

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def test_cache_a_package_from_pypi(self):
        response = self.fetch(self._url_for(NAME, VERSION), method='POST', body='')

        assert_that(response.code, is_(httplib.CREATED))
        assert_that(response.headers, has_entry('Location', '/packages/%s/%s' % (NAME, VERSION)))
        assert_that_method(self.cache.cache_package).was_called()

    def test_cache_a_non_existing_package_from_pypi_returns_not_found(self):
        when(self.cache.cache_package).then_raise(errors.NotFoundError())

        response = self.fetch(self._url_for(NAME, INEXISTENT_VERSION), method='POST', body='')

        assert_that(response.code, is_(httplib.NOT_FOUND))

    def test_cache_a_package_from_pypi_returns_conflict_if_already_exists(self):
        when(self.cache.cache_package).then_raise(errors.AlreadyExistsError)

        response = self.fetch(self._url_for(NAME, VERSION), method='POST', body='')

        assert_that(response.code, is_(httplib.CONFLICT))

    def _url_for(self, id_, version):
        return '/packages/%s/%s' % (id_, version)

    def get_app(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))
        self.cache = spy(cache.Cache(self.packages, None, None))

        return web.Application([
                web.url(r'/packages/(?P<id_>%s)' % viper.identifier(),
                    handlers.PackageHandler, dict(packages=self.packages, cache=self.cache),
                    name='package'
                ),
                web.url(r'/packages/(?P<id_>%s)/(?P<version>%s)' % (viper.identifier(), viper.identifier()),
                    handlers.PackageHandler, dict(packages=self.packages, cache=self.cache),
                    name='package_with_version'
                ),
                web.url(r'/packages',
                    handlers.AllPackagesHandler, dict(packages=None),
                    name='packages'
                )
            ],
            debug=True,
            template_path=os.path.join(os.path.dirname(handlers.__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(handlers.__file__), 'static')
        )
