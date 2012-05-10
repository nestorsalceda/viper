# -*- coding: utf-8 -*-

import httplib
import datetime
import urlparse
import functools

from pymongo import son_manipulator, errors, ASCENDING
import gridfs

from tornado import httpclient, escape

from viper import entities


class NotFoundError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class PackageMapper(object):

    def __init__(self, database):
        self.database = database
        self._collection = None

    def _packages(self):
        if self._collection is None:
            self.database.add_son_manipulator(Manipulator())
            self._collection = self.database.packages
            self._collection.create_index(u'name', unique=True)

        return self._collection

    def get_by_name(self, name):
        result = self._packages().find_one({u'name': name})
        if not result:
            raise NotFoundError()

        return result

    def store(self, package):
        query = {'package': package}
        if package.id_ is not None:
            query['_id'] = package.id_
            package.last_updated_on = datetime.datetime.utcnow()

        try:
            package.id_ = self._packages().save(query, safe=True)
        except errors.DuplicateKeyError:
            raise AlreadyExistsError()

    def all(self):
        return self._packages().find(sort=[('name', ASCENDING)])

    def count_all(self):
        return self.all().count()

    def exists(self, name):
        return self._packages().find({'name': name}).count() != 0


class FileMapper(object):

    def __init__(self, database):
        self.database = database
        self._collection = None

    def _files(self):
        if self._collection is None:
            self._collection = gridfs.GridFS(self.database)

        return self._collection

    def store(self, filename, content):
        if self._files().exists(filename):
            raise AlreadyExistsError()

        self._files().put(content, _id=filename, filename=filename)

    def get_by_name(self, filename):
        if not self._files().exists(filename):
            raise NotFoundError()

        return self._files().get(filename).read()


class PythonPackageIndex(object):

    URL = u'http://pypi.python.org/pypi/%s/json'

    def __init__(self):
        self._httpclient = httpclient.HTTPClient()

    def get_by_name(self, name):
        response = self._query_pypi(name)

        package = entities.Package(name)
        package.is_from_pypi = True
        release = entities.Release(response['info'][u'version'])

        for key, value in response['info'].iteritems():
            if hasattr(release, key) and value != 'UNKNOWN':
                setattr(release, key, value)

        package.store_release(release)
        return package

    def _query_pypi(self, name):
        try:
            response = self._httpclient.fetch(self.URL % name)
            return escape.json_decode(response.body)
        except httpclient.HTTPError as error:
            if error.code == httplib.NOT_FOUND:
                raise NotFoundError()

    def download_files(self, name, on_file_downloaded):

        def _on_file_downloaded_from_url(url, response):
            on_file_downloaded(
                entities.File(url[u'filename'], url[u'packagetype'], url[u'md5_digest']),
                response.body
            )

        def _on_file_downloaded_from_download_url(url, response):
            filename = urlparse.urlparse(url)[2].split(u'/')[-1]
            on_file_downloaded(
                entities.File(filename, u'sdist', None),
                response.body
            )

        response = self._query_pypi(name)
        client = httpclient.AsyncHTTPClient()

        if not response[u'urls']:
            url = response[u'info'][u'download_url']
            client.fetch(url, functools.partial(_on_file_downloaded_from_download_url, url))
        else:
            for url in response[u'urls']:
                client.fetch(url[u'url'], functools.partial(_on_file_downloaded_from_url, url))


class Manipulator(son_manipulator.SONManipulator):

    def transform_incoming(self, son, collection):
        for key, value in son.items():
            if isinstance(value, entities.Package):
                return self._serialize_package(value)
            elif isinstance(value, dict):
                son[key] = self.transform_incoming(value, collection)

        return son

    def _serialize_package(self, package):
        result = dict(package.__dict__)
        del result[u'_releases']

        if result[u'_id'] is None:
            del result['_id']

        result[u'releases'] = [self._serialize_release(release) for release in package.releases()]
        return result

    def _serialize_release(self, release):
        result = dict(release.__dict__)
        result[u'files'] = self._serialize_files(release)

        return result

    def _serialize_files(self, release):
        return [dict(file_.__dict__) for file_ in release.files.values()]

    def transform_outgoing(self, son, collection):
        if collection.name == u'packages' and isinstance(son, dict):
            return self._deserialize_package(son)

        return son

    def _deserialize_package(self, result):
        package = entities.Package(result[u'name'])
        self._inject_fields(package, result, exclude=[u'releases'])

        for release in result[u'releases']:
            package.store_release(self._deserialize_release(release))

        return package

    def _inject_fields(self, obj, result, exclude=[]):
        for key, value in result.iteritems():
            if hasattr(obj, key) and key not in exclude:
                setattr(obj, key, value)

        return obj

    def _deserialize_release(self, result):
        release = entities.Release(result[u'version'])
        self._inject_fields(release, result, exclude=[u'files'])

        for file_ in result[u'files']:
            release.add_file(entities.File(file_[u'name'], file_[u'filetype'], file_['md5_digest']))

        return release
