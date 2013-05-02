# -*- coding: utf-8 -*-

import datetime

from mamba import describe, context, before
from sure import expect

from viper import errors
from viper.entities import Package, Release

NAME = u'viper'
VERSION = u'0.1dev'
OLDER_VERSION = u'0.0.1'
NEWER_VERSION = u'1.0'


with describe('Package') as _:

    @before.each
    def create_new_package():
        _.package = Package(NAME)

    def it_should_have_name():
        expect(_.package.name).to.be.equal(NAME)

    def it_should_have_created_on_date():
        expect(_.package.created_on).to.be.a(datetime.datetime)

    def it_should_have_last_updated_on_date():
        expect(_.package.last_updated_on).to.be.a(datetime.datetime)

    def it_should_not_be_from_pypi():
        expect(_.package.is_from_pypi).to.be.false

    with context('when getting a release'):
        def it_should_raise_an_error_if_a_version_does_not_exist():
            expect(_.package.release).when.called_with(VERSION).throw(errors.NotFoundError)

        def it_should_get_a_release_if_version_exists():
            release = Release(VERSION)
            _.package.store_release(release)

            expect(_.package.release(VERSION)).to.be.equal(release)

        def it_should_return_releases_ordered_by_version():
            _.package.store_release(Release(VERSION))
            _.package.store_release(Release(NEWER_VERSION))
            _.package.store_release(Release(OLDER_VERSION))

            releases = _.package.releases()

            expect([release.version for release in releases]).to.be.equal([NEWER_VERSION, VERSION, OLDER_VERSION])

        def it_should_return_newer_as_last_version():
            _.package.store_release(Release(VERSION))
            _.package.store_release(Release(NEWER_VERSION))
            _.package.store_release(Release(OLDER_VERSION))

            expect(_.package.last_release().version).to.be.equal(NEWER_VERSION)

    with context('when checking if a release exists'):
        def it_should_not_have_a_release_unless_stored():
            expect(_.package.has_release(Release(VERSION))).to.be.false
            expect(_.package.has_release(VERSION)).to.be.false

        def it_should_have_a_release_if_stored():
            _.package.store_release(Release(VERSION))

            expect(_.package.has_release(Release(VERSION))).to.be.true
            expect(_.package.has_release(VERSION)).to.be.true

