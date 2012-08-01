# -*- coding: utf-8 -*-

import functools
import logging

from viper import errors

class Cache(object):

    def __init__(self, packages, files, pypi):
        self.packages = packages
        self.files = files
        self.pypi = pypi

    def cache_package(self, id_, version=None):
        package = from_pypi = self.pypi.get_by_name(id_, version)

        if self.packages.exists(id_):
            package = self.packages.get_by_name(id_)
            if package.has_release(from_pypi.last_release()):
                raise errors.AlreadyExistsError()
            package.store_release(from_pypi.last_release())
            self.packages.store(package)
        else:
            self.packages.store(from_pypi)

        on_file_downloaded = functools.partial(self._on_file_downloaded, package, version)
        self.pypi.download_files(id_, version=version, on_file_downloaded=on_file_downloaded)

    def _on_file_downloaded(self, package, version, file_, content):
        logging.info('Downloaded %s', file_.name)
        self.files.store(file_.name, content)

        if version is None:
            package.last_release().add_file(file_)
        else:
            package.release(version).add_file(file_)

        self.packages.store(package)
