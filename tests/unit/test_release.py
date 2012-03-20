# -*- coding: utf-8 -*-

import datetime

from hamcrest import *

from viper.entities import Release

VERSION = u'0.1dev'


class TestRelease(object):

    def setup(self):
        self.release = Release(VERSION)

    def test_release_has_metadata_when_created(self):
        assert_that(self.release.version, is_(VERSION))
        assert_that(self.release.created_on, is_(datetime.datetime))
