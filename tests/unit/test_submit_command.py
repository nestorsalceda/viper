# -*- coding: utf-8 -*-

from pyDoubles.framework import *
from hamcrest import *

from viper.commands import SubmitCommand
from viper import mappers, errors


class TestSubmitCommand(object):

    def setup(self):
        self.packages = spy(mappers.PackageMapper(empty_stub()))
        self.command = SubmitCommand(self.packages)

    def test_create_new_package(self):
        when(self.packages.get_by_name).then_raise(errors.NotFoundError())

        self.command.execute(
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

        assert_that_method(self.packages.store).was_called()
