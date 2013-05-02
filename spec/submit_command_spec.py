# -*- coding: utf-8 -*-

from mamba import describe
from sure import expect
from doublex import *

from viper.commands import SubmitCommand
from viper import mappers, errors


with describe('SubmitCommand'):

    def it_should_create_new_package_if_not_exists():
        repository = Spy(mappers.PackageMapper(None))
        command = SubmitCommand(repository)

        with repository:
            repository.get_by_name(ANY_ARG).raises(errors.NotFoundError())

        command.execute(
            license=u'MIT/X11',
            name=u'viper',
            author=u'Néstor Salceda',
            home_page=None,
            download_url=None,
            summary=None,
            author_email=u'nestor.salceda@gmail.com',
            version=u'0.1dev',
            platform=None,
            keywords=None,
            classifiers=[],
            description=None
        )

        expect(called().matches(repository.store)).to.be.true
