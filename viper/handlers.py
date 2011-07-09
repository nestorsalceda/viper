# -*- coding: utf-8 -*-

from tornado import web


class MainHandler(web.RequestHandler):

    def get(self):
        self.render('main.html')
