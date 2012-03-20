# -*- coding: utf-8 -*-


class PackageNotFoundError(Exception):
    pass


class PackageMapper(object):

    def __init__(self, database):
        self.collection = database.packages

    def get_by_name(self, name):
        pass

    def store(self, package):
        pass
