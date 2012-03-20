# -*- coding: utf-8 -*-

from tornado import web, httputil


class MainHandler(web.RequestHandler):

    def get(self):
        self.render(u'main.html')


class DistutilsHandler(web.RequestHandler):

    def initialize(self, distutils_commands):
        self.distutils_commands = distutils_commands

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

    def post(self):
        action = self.get_argument(u':action')

        command = self.distutils_commands.command_for(action)
        command.execute(**self._distutils_arguments())

    def _distutils_arguments(self):
        arguments = self.request.arguments.keys()

        result = dict([(key, self._argument_if_not_is_unknown_or_empty(key)) for key in arguments])

        result[u'classifiers'] = self.get_arguments(u'classifiers')

        self._delete_field(result, u'metadata_version')
        self._delete_field(result, u':action')
        self._delete_field(result, u'protcol_version')

        return result

    def _argument_if_not_is_unknown_or_empty(self, argument):
        value = self.get_argument(argument)
        if not value or value == u'UNKNOWN':
            value = None
        return value

    def _delete_field(self, fields, field):
        if field in fields:
            del fields[field]
