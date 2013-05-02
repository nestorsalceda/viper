# -*- coding: utf-8 -*-

from mamba import describe, context, before
from sure import expect
from doublex import *

from viper import mappers, cache, errors, entities

PACKAGE = u'tornado'
PYPI_RELEASE = u'2.0'
CACHED_RELEASE = u'1.0'


with describe('Cache') as _:

    @before.each
    def create_repositories_and_cache():
        _.package_repository = Spy(mappers.PackageMapper(None))
        _.file_repository = Spy(mappers.PackageMapper(None))
        _.pypi = Spy(mappers.PythonPackageIndex())

        _.cache = cache.Cache(_.package_repository, _.file_repository, _.pypi)

    with context('when caches a package'):
        @before.each
        def cache_package():
            _.cache.cache_package(PACKAGE)

        def it_should_ask_pypi_and_store_and_download_its_files():
            expect(called().with_args(PACKAGE, None).matches(_.pypi.get_by_name)).to.be.true

        def it_should_store_the_package():
            expect(called().matches(_.package_repository.store)).to.be.true

        def it_should_download_files_from_pypi():
            expect(called().matches(_.pypi.download_files))

    def it_should_raise_not_found_error_unless_found_in_pypi():
        with _.pypi:
            _.pypi.get_by_name(PACKAGE).raises(errors.NotFoundError())

        expect(_.cache.cache_package).when.called_with(PACKAGE, ANY_ARG).to.throw(errors.NotFoundError)

    def it_should_overwrite_cached_package():
        existing = _an_existing_package()
        with _.package_repository:
            _.package_repository.exists(PACKAGE).returns(True)
            _.package_repository.get_by_name(PACKAGE).returns(existing)

        with _.pypi:
            _.pypi.get_by_name(ANY_ARG).returns(_a_pypi_package())

        _.cache.cache_package(PACKAGE)

        expect(existing.has_release(CACHED_RELEASE)).to.be.true
        expect(existing.has_release(PYPI_RELEASE)).to.be.true

    def _a_pypi_package():
        package = entities.Package(PACKAGE)
        package.store_release(entities.Release(PYPI_RELEASE))

        return package

    def _an_existing_package():
        package = entities.Package(PACKAGE)
        package.store_release(entities.Release(CACHED_RELEASE))

        return package

    def it_should_raise_an_error_if_specified_version_was_already_cached():
        with _.package_repository:
            _.package_repository.exists(PACKAGE).returns(True)
            _.package_repository.get_by_name(PACKAGE).returns(_an_existing_package_with_pypi_version())

        with _.pypi:
            _.pypi.get_by_name(ANY_ARG).returns(_a_pypi_package())

        expect(_.cache.cache_package).when.called_with(PACKAGE, PYPI_RELEASE).to.throw(errors.AlreadyExistsError)

    def _an_existing_package_with_pypi_version():
        cached = _an_existing_package()
        cached.store_release(_a_pypi_package().last_release())

        return cached
