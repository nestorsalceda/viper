# -*- coding: utf-8 -*-

import datetime

from docutils import core
from docutils.writers import html4css1

from viper import errors


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
        self.classifiers = []
        self.files = {}

    def add_file(self, file_):
        if file_.name in self.files:
            raise errors.AlreadyExistsError("File with name %s already exists in this release" % file_.name)


        self.files[file_.name] = file_

    def html_description(self):
        if self.description is None:
            return None

        return core.publish_parts(self.description, writer=html4css1.Writer())['html_body']


class Package(object):

    def __init__(self, name):
        now = datetime.datetime.utcnow()

        self._id = None
        self.name = name
        self.created_on = now
        self.last_updated_on = now
        self.is_from_pypi= False
        self._releases = {}

    def store_release(self, release):
        self._releases[release.version] = release

    def release(self, version):
        if not version in self._releases:
            raise errors.NotFoundError("Release with version %s doesn't exist for this package" % version)

        return self._releases[version]

    def releases(self):
        return self._releases.values()

    def last_release(self):
        return self.release(self._releases.keys()[0])

    def has_release(self, release):
        if isinstance(release, basestring):
            return release in self._releases

        return release.version in self._releases

    def __eq__(self, other):
        return self.id_ == other.id_

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value
