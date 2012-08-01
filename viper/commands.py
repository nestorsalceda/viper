# -*- coding: utf-8 -*-

from viper.entities import Package, Release, File
from viper import errors


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
        except errors.NotFoundError:
            return Package(name)

    def _release(self, **kwargs):
        release = Release(kwargs[u'version'])

        for key, value in kwargs.iteritems():
            if hasattr(release, key):
                setattr(release, key, value)

        return release


class FileUploadCommand(Command):

    def __init__(self, packages, files):
        self.packages = packages
        self.files = files

    def execute(self, **kwargs):
        self._associate_file_to_package(**kwargs)
        self._store_raw(kwargs['uploaded_file'])

    def _associate_file_to_package(self, **kwargs):
        package = self.packages.get_by_name(kwargs[u'name'])
        release = package.release(kwargs[u'version'])

        uploaded = kwargs['uploaded_file']
        release.add_file(File(
            uploaded['filename'],
            kwargs['filetype'],
            kwargs['md5_digest']
        ))

        self.packages.store(package)

    def _store_raw(self, uploaded):
        self.files.store(uploaded['filename'], uploaded['body'])
