# -*- coding: utf-8 -*-

from hamcrest import *
from nose.tools import raises

import pymongo

from viper import mappers
from viper.entities import Package, Release


NAME = u'viper'
VERSION = u'0.1dev'

class TestPackageMapper(object):

    def test_insert_new_package(self):
        new = Package(NAME)

        self.mapper.store(new)

        retrieved = self.mapper.get_by_name(NAME)
        assert_that(retrieved, is_(new))

    def test_update_package(self):
        new = Package(NAME)
        self.mapper.store(new)

        new.store_release(Release(VERSION))
        self.mapper.store(new)

        retrieved = self.mapper.get_by_name(NAME)
        assert_that(retrieved, is_(new))

    @raises(mappers.PackageNotFoundError)
    def test_raise_error_unless_found(self):
        self.mapper.get_by_name(NAME)

    def setup(self):
        self.database = pymongo.Connection()['viper_package_index_test']
        self.cleanup()

        self.mapper = mappers.PackageMapper(self.database)

    def cleanup(self):
        self.database.drop_collection(self.database.packages)
