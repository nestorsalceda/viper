# -*- coding: utf-8 -*-

from hamcrest import *
from pyDoubles.framework import *
from nose.tools import assert_raises

from viper import mappers, cache, errors, entities

PACKAGE = u'tornado'
PYPI_RELEASE = u'2.0'
CACHED_RELEASE = u'1.0'


class TestCache(object):

    def test_cache_package(self):
        self.cache.cache_package(PACKAGE)

        assert_that_method(self.pypi.get_by_name).was_called().with_args(PACKAGE, None)
        assert_that_method(self.packages.store).was_called()
        assert_that_method(self.pypi.download_files).was_called()

    def test_cache_package_raises_error_if_not_found_in_pypi(self):
        when(self.pypi.get_by_name).then_raise(errors.NotFoundError())

        with assert_raises(errors.NotFoundError):
            self.cache.cache_package(PACKAGE)

    def test_updates_cached_package(self):
        when(self.pypi.get_by_name).then_return(self._pypi())
        when(self.packages.exists).then_return(True)
        cached = self._cached()
        when(self.packages.get_by_name).then_return(cached)

        self.cache.cache_package(PACKAGE)

        assert_that(cached.has_release(CACHED_RELEASE))
        assert_that(cached.has_release(PYPI_RELEASE))

    def _pypi(self):
        package = entities.Package(PACKAGE)
        package.store_release(entities.Release(PYPI_RELEASE))

        return package

    def _cached(self):
        package = entities.Package(PACKAGE)
        package.store_release(entities.Release(CACHED_RELEASE))

        return package

    def test_raises_an_error_if_specified_version_already_exists_in_cached_package(self):
        when(self.pypi.get_by_name).then_return(self._pypi())
        when(self.packages.exists).then_return(True)
        when(self.packages.get_by_name).then_return(self._cached_with_pypi_version())

        with assert_raises(errors.AlreadyExistsError):
            self.cache.cache_package(PACKAGE, PYPI_RELEASE)

    def _cached_with_pypi_version(self):
        cached = self._cached()
        cached.store_release(self._pypi().last_release())

        return cached

    def setup(self):
        self.packages = spy(mappers.PackageMapper(None))
        self.files = spy(mappers.PackageMapper(None))
        self.pypi = spy(mappers.PythonPackageIndex())

        self.cache = cache.Cache(self.packages, self.files, self.pypi)

