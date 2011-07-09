# -*- coding: utf-8 -*-

class CommandFactory(object):
    def command_for(self, action):
        return Command()

class Command(object):
    def execute(self, **kwargs):
        raise NotImplementedError()
