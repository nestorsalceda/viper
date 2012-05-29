# -*- coding: utf-8 -*-

from pyDoubles.framework import *
from nose.tools import assert_raises

from viper import mappers, cache

PACKAGE = u'tornado'


class TestCache(object):

    def test_cache_package(self):
        self.cache.cache_package(PACKAGE)

        assert_that_method(self.pypi.get_by_name).was_called().with_args(PACKAGE)
        assert_that_method(self.packages.store).was_called()
        assert_that_method(self.pypi.download_files).was_called()

    def test_cache_package_raises_error_if_not_found_in_pypi(self):
        when(self.pypi.get_by_name).then_raise(mappers.NotFoundError())

        with assert_raises(mappers.NotFoundError):
            self.cache.cache_package(PACKAGE)

    def setup(self):
        self.packages = spy(mappers.PackageMapper(None))
        self.files = spy(mappers.PackageMapper(None))
        self.pypi = spy(mappers.PythonPackageIndex())

        self.cache = cache.Cache(self.packages, self.files, self.pypi)

