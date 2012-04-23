# -*- coding: utf-8 -*-

import httplib

from tornado import web, httputil

from viper import commands, mappers


class MainHandler(web.RequestHandler):

    def get(self):
        self.render(u'main.html')


class DistutilsHandler(web.RequestHandler):

    def initialize(self, submit, upload):
        self.submit = submit
        self.upload = upload

    def prepare(self):
        self._parse_distutils_message()

    def _parse_distutils_message(self):
        # http://groups.google.com/group/python-tornado/browse_thread/thread/d0531e331c189c56?pli=1

        httputil.parse_multipart_form_data(
            self._boundary(),
            self.request.body.replace("\n", "\r\n"),
            self.request.arguments,
            self.request.files
        )

    def _boundary(self):
        content_types = self.request.headers['Content-Type'].split(';')
        for field in content_types:
            if 'boundary=' in field:
                return field.split('=')[1]

    def _uploaded_file(self):
        if 'content' not in self.request.files:
            return None

        uploaded = self.request.files['content'][0]
        # As we replaced lf with cr + lf for parsing http body, uploaded file
        # was modified too.  We replace to original for avoding corruption
        uploaded['body'] = uploaded['body'].replace('\r\n', '\n')

        return uploaded

    def post(self):
        command = self._choose_command()
        command.execute(**self._distutils_arguments())

    def _choose_command(self):
        action = self.get_argument(':action')
        if action == u'submit':
            return self.submit
        elif action == u'file_upload':
            return self.upload
        else:
            return commands.Command()

    def _distutils_arguments(self):
        arguments = self.request.arguments.keys()

        result = dict([(key, self._argument_if_not_is_unknown_or_empty(key)) for key in arguments])

        result[u'classifiers'] = self.get_arguments(u'classifiers')

        self._delete_field(result, u'metadata_version')
        self._delete_field(result, u':action')
        self._delete_field(result, u'protcol_version')

        result[u'uploaded_file'] = self._uploaded_file()

        return result

    def _argument_if_not_is_unknown_or_empty(self, argument):
        value = self.get_argument(argument)
        if not value or value == u'UNKNOWN':
            value = None
        return value

    def _delete_field(self, fields, field):
        if field in fields:
            del fields[field]


class PackageHandler(web.RequestHandler):

    def initialize(self, packages):
        self.packages = packages

    def get(self, id_):
        try:
            package = self.packages.get_by_name(id_)
            self.render('package.html', package=package, last_release=package.last_release())
        except mappers.NotFoundError:
            raise web.HTTPError(httplib.NOT_FOUND)
