#!/usr/bin/env python

import os
import logging

from tornado import ioloop, options
from viper import application

options.define('address', default='127.0.0.1', help='listen in given address', type=str)
options.define('port', default=os.environ.get('PORT', 3000), help='run on the given port', type=int)
options.define('mongodb_host', default=os.environ.get('MONGOHQ_URL', "mongodb://127.0.0.1:27017"), type=str)
options.define('mongodb_database', default=os.environ.get('MONGOHQ_URL', "viper_package_index"), type=str)

logger = logging.getLogger(__file__)

if __name__ == '__main__':
    try:
        options.parse_command_line()
        application(mongodb={
            'host': options.options.mongodb_host,
            'database': options.options.mongodb_database.split('/')[-1]
        }).listen(options.options.port, address=options.options.address)
        logger.info('Listening on: %s:%s', options.options.address, options.options.port)
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info('Shutting down the server')
