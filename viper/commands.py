# -*- coding: utf-8 -*-

from viper.entities import Package, Release
from viper.mappers import PackageMapper, PackageNotFoundError


class Command(object):

    def execute(self, **kwargs):
        raise NotImplementedError()


class SubmitCommand(Command):

    def __init__(self, packages):
        self.packages = packages

    def execute(self, **kwargs):
        package = self._get_or_create_new(kwargs[u'name'])
        package.store_release(self._release(**kwargs))

        self.packages.store(package)

    def _get_or_create_new(self, name):
        try:
            return self.packages.get_by_name(name)
        except PackageNotFoundError:
            return Package(name)

    def _release(self, **kwargs):
        release = Release(kwargs[u'version'])

        for key, value in kwargs.iteritems():
            if hasattr(release, key):
                setattr(release, key, value)

        return release


class FileUploadCommand(Command):
    pass


class CommandFactory(object):

    def __init__(self, connection):
        self.connection = connection

    def _registry(self):
        return {
            u'submit': SubmitCommand(PackageMapper(self.connection)),
            u'file_upload': FileUploadCommand()
        }

    def command_for(self, action):
        return self._registry().get(action, Command())
