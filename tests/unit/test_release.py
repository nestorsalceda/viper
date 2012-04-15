# -*- coding: utf-8 -*-

import datetime

from hamcrest import *
from nose.tools import assert_raises

from viper.entities import Release, File

VERSION = u'0.1dev'
FILE_NAME = u'viper-0.1dev.tar.gz'
FILE_TYPE = u'sdist'
MD5_DIGEST = u'06022cad9c65a8aa384ce8df1ce6f6d9'


class TestRelease(object):

    def setup(self):
        self.release = Release(VERSION)

    def test_release_has_metadata_when_created(self):
        assert_that(self.release.version, is_(VERSION))
        assert_that(self.release.created_on, is_(datetime.datetime))

    def test_upload_a_file(self):
        uploaded = File(
            FILE_NAME,
            FILE_TYPE,
            MD5_DIGEST
        )

        self.release.upload(uploaded)

        assert_that(self.release.files, has_entry(FILE_NAME, uploaded))

    def test_upload_an_existent_file_raises_error(self):
        uploaded = File(
            FILE_NAME,
            FILE_TYPE,
            MD5_DIGEST
        )
        self.release.upload(uploaded)

        with assert_raises(ValueError):
            self.release.upload(uploaded)
