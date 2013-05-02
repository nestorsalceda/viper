# -*- coding: utf-8 -*-

import datetime

from mamba import describe, context, before
from sure import expect

from viper.entities import Release, File
from viper import errors

import docutils

NEWER_VERSION = u'2.0'
VERSION = u'0.1dev'
FILE_NAME = u'viper-0.1dev.tar.gz'
FILE_TYPE = u'sdist'
MD5_DIGEST = u'06022cad9c65a8aa384ce8df1ce6f6d9'


with describe('Release') as _:
    @before.each
    def create_release():
        _.release = Release(VERSION)

    def it_should_have_version():
        expect(_.release.version).to.be.equal(VERSION)

    def it_should_have_created_on_date():
        expect(_.release.created_on).to.be.a(datetime.datetime)

    with context('when adding a file'):
        @before.each
        def create_and_add_a_file():
            _.uploaded = File(FILE_NAME, FILE_TYPE, MD5_DIGEST)

            _.release.add_file(_.uploaded)

        def it_should_have_the_added_file():
            expect(_.release.files).to.have.key(FILE_NAME).being.equal(_.uploaded)

        def it_should_raise_an_error_if_same_file_already_exists():
            expect(_.release.add_file).when.called_with(_.uploaded).to.throw(errors.AlreadyExistsError)

    with context('when generating description as html'):
        #TODO: Extract a HTMLGenerator

        def it_should_contain_description_in_html():
            _.release.description = 'This package aims to integrate Mercurial and Status.net.'

            expect(_.release.description).to.be.within(_.release.html_description())

        def it_should_be_none_if_empty():
            expect(_.release.html_description()).to.be.none

        def it_should_raise_error_if_html_description_has_errors():
            _.release.description = u'''Section Title
    ============'''

            expect(_.release.html_description).when.called.to.throw(docutils.utils.SystemMessage)

    with context('when comparing versions'):
         def it_should_be_older_than_newer_version():
            newer = Release(NEWER_VERSION)

            expect(_.release).to.be.lower_than(newer)

