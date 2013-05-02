# -*- coding: utf-8 -*-

from mamba import describe
from sure import expect
from doublex import *

from viper.commands import FileUploadCommand
from viper.mappers import PackageMapper, FileMapper
from viper.entities import Package, Release

NAME = u'viper'
VERSION = u'0.1dev'
FILE_CONTENT = u'content'
FILE_NAME = u'viper-0.1dev.tar.gz'


with describe('FileUploadCommand'):
    def it_should_upload_file_for_an_existent_package():
        package_repository = Spy(PackageMapper(None))
        file_repository = Spy(FileMapper(None))
        command = FileUploadCommand(package_repository, file_repository)

        package = Package(NAME)
        package.store_release(Release(VERSION))
        with package_repository:
            package_repository.get_by_name(ANY_ARG).returns(package)

        command.execute(
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

        expect(called().matches(package_repository.store)).to.be.true
        expect(called().with_args(FILE_NAME, FILE_CONTENT).matches(file_repository.store)).to.be.true
