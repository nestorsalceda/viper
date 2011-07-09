# -*- coding: utf-8 -*-

from tornado import web, httputil


class MainHandler(web.RequestHandler):

    def get(self):
        self.render('main.html')


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
            {}
        )

    def _boundary(self):
        content_types = self.request.headers['Content-Type'].split(';')
        for field in content_types:
            if 'boundary=' in field:
                return field.split('=')[1]

    def post(self):
        action = self.get_argument(':action')

        command = self.distutils_commands.command_for(action)
        command.execute()


