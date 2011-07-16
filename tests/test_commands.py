# -*- coding: utf-8 -*-

from hamcrest import *
from pyDoubles.framework import *

from viper import commands


class TestCommandFactory(object):

    INVALID = 'invalid_action'
    SUBMIT = 'submit'
    FILE_UPLOAD = 'file_upload'

    def setup(self):
        self.factory = commands.CommandFactory(empty_stub())

    def test_default_command_for_invalid_action(self):
        assert_that(
            self.factory.command_for(self.INVALID),
            instance_of(commands.Command)
        )

    def test_command_for_submit_action(self):
        assert_that(
            self.factory.command_for(self.SUBMIT),
            instance_of(commands.SubmitCommand)
        )

    def test_command_for_file_upload_action(self):
        assert_that(
            self.factory.command_for(self.FILE_UPLOAD),
            instance_of(commands.FileUploadCommand)
        )
