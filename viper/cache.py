# -*- coding: utf-8 -*-

import functools
import logging


class Cache(object):

    def __init__(self, packages, files, pypi):
        self.packages = packages
        self.files = files
        self.pypi = pypi

    def cache_package(self, id_):
        package = self.pypi.get_by_name(id_)
        self.packages.store(package)

        on_file_downloaded = functools.partial(self._on_file_downloaded, package)
        self.pypi.download_files(id_, on_file_downloaded)

    def _on_file_downloaded(self, package, file_, content):
        logging.info('Downloaded %s', file_.name)
        self.files.store(file_.name, content)
        package.last_release().add_file(file_)
        self.packages.store(package)
