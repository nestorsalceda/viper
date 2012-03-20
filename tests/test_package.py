# -*- coding: utf-8 -*-

import datetime

from hamcrest import *
from nose.tools import raises

from viper.entities import Package, Release

NAME = u'viper'
VERSION = u'0.1dev'
AUTHOR = u'Néstor Salceda'


class TestPackage(object):

    def setup(self):
        self.package = Package(NAME)

    def test_package_has_metadata_when_created(self):
        assert_that(self.package.name, is_(NAME))
        assert_that(self.package.created_on, is_(datetime.datetime))
        assert_that(self.package.last_updated_on, is_(datetime.datetime))

    @raises(ValueError)
    def test_getting_inexistent_release_raises_error(self):
        self.package.release(VERSION)

    def test_package_sets_new_release(self):
        release = Release(VERSION)
        self.package.store_release(release)

        assert_that(self.package.release(VERSION), is_(release))

    def test_package_sets_existent_release_replaces_it(self):
        self.package.store_release(Release(VERSION))
        self.package.store_release(Release(VERSION))

        assert_that(self.package.releases(), has_length(1))
