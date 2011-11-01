# -*- coding: utf-8 -*-

class Command(object):
    def execute(self, **kwargs):
        raise NotImplementedError()

class SubmitCommand(Command):
    pass

class FileUploadCommand(Command):
    pass

class CommandFactory(object):
    _COMMANDS = {
        'submit': SubmitCommand(),
        'file_upload': FileUploadCommand()
    }

    def command_for(self, action):
        return self._COMMANDS.get(action, Command())

