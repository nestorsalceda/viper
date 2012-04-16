#!/usr/bin/env python

import logging

from tornado import ioloop, options
from viper import application

options.define('port', default=3000, help='run on the given port', type=int)

logger = logging.getLogger(__file__)

if __name__ == '__main__':
    try:
        options.parse_command_line()
        application().listen(options.options.port)
        logger.info('Listening on port: %s', options.options.port)
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info('Shutting down the server')
