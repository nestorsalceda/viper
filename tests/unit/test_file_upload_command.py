# -*- coding: utf-8 -*-

from pyDoubles.framework import *
from hamcrest import *

from viper.commands import FileUploadCommand
from viper.mappers import PackageMapper, FileMapper
from viper.entities import Package, Release

NAME = u'viper'
VERSION = u'0.1dev'
FILE_CONTENT = u'content'
FILE_NAME = u'viper-0.1dev.tar.gz'


class TestFileUploadCommand(object):

    def setup(self):
        self.packages = spy(PackageMapper(empty_stub()))
        self.files = spy(FileMapper())
        self.command = FileUploadCommand(self.packages, self.files)

    def test_upload_file_for_existent_package(self):
        package = Package(NAME)
        package.store_release(Release(VERSION))
        when(self.packages.get_by_name).then_return(package)

        self.command.execute(
            name=NAME,
            version=VERSION,
            filetype=u'sdist',
            md5_digest=u'06022cad9c65a8aa384ce8df1ce6f6d9',
            uploaded_file={
                'body': FILE_CONTENT,
                'content_type': 'application/unknown',
                'filename': FILE_NAME,
            }
        )

        assert_that_method(self.packages.store).was_called()
        assert_that_method(self.files.store).was_called().with_args(
            FILE_NAME,
            FILE_CONTENT
        )
