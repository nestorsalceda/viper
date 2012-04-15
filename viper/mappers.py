# -*- coding: utf-8 -*-

from pymongo import son_manipulator

from viper import entities


class PackageNotFoundError(Exception):
    pass


class PackageMapper(object):

    def __init__(self, database):
        database.add_son_manipulator(Manipulator())
        self.collection = database.packages

    def get_by_name(self, name):
        result = self.collection.find_one({u'name': name})
        if not result:
            raise PackageNotFoundError()

        return result

    def store(self, package):
        query = {'package': package}
        if package.id_ is not None:
            query['_id'] = package.id_

        package.id_ = self.collection.save(query)


class FileMapper(object):

    def store(self, filename, content):
        pass


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
        del result[u'files']

        return result

    def transform_outgoing(self, son, collection):
        if isinstance(son, dict):
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
        return self._inject_fields(release, result)
