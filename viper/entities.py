# -*- coding: utf-8 -*-

import datetime


class File(object):
    def __init__(self, name, filetype, md5_digest):
        self.name = name
        self.filetype = filetype
        self.md5_digest = md5_digest


class Release(object):
    def __init__(self, version):
        self.version = version
        self.created_on = datetime.datetime.utcnow()
        self.license = None
        self.author = None
        self.author_email = None
        self.home_page = None
        self.download_url = None
        self.summary = None
        self.description = None
        self.keywords = None
        self.classifiers = None
        self.files = {}

    def add_file(self, file_):
        if file_.name in self.files:
            raise ValueError

        self.files[file_.name] = file_


class Package(object):

    def __init__(self, name):
        now = datetime.datetime.utcnow()

        self._id = None
        self.name = name
        self.created_on = now
        self.last_updated_on = now
        self._releases = {}

    def store_release(self, release):
        self._releases[release.version] = release

    def release(self, version):
        if not version in self._releases:
            raise ValueError()

        return self._releases[version]

    def releases(self):
        return self._releases.values()

    def __eq__(self, other):
        return self.id_ == other.id_

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value
