# -*- coding: ISO-8859-2 -*-
"""
This script runs the LunchVoting application using a development server.
"""

import os

from LunchVoting import app

if __name__ == '__main__':
    print(' * Reading configuration')
    app.config.update(dict(
        DATABASE = os.environ.get('VFLV_DATABASE', 'vflv.db'),
        BAD_USER = os.environ.get('BAD_USER', 'buc1'),
        DEBUG = int(os.environ.get('VFLV_DEBUG', '0')),
        PORT = int(os.environ.get('VFLV_SERVER_PORT', '5555')),
        HOST = os.environ.get('VFLV_SERVER_HOST', 'localhost'),
        SECRET_KEY = os.environ.get('VFLV_SECRET_KEY', 
            '\xed\x8ege\xea}\x03\xc0\x8c$$\x98\xa4N\xa8\xb6\xf0k\x8a\x86\xe4\xa9\x19\xb7\x8a$'),
        # required version
        DATABASE_VERSION = int(os.environ.get('VFLV_DATABASE_VERSION', '2'))
        ))
    app.config.from_envvar('VFLV_SETTINGS', silent=True)
    print(app.config)
    print(' * Starting the server')
    app.run(host=app.config['HOST'], port=app.config['PORT'])
