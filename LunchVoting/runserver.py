# -*- coding: ISO-8859-2 -*-
"""
This script runs the LunchVoting application using a development server.
"""

import os

from LunchVoting import app

if __name__ == '__main__':
    DEBUG = int(os.environ.get('VFLV_DEBUG', '0'))
    PORT = int(os.environ.get('VFLV_SERVER_PORT', '5555'))
    HOST = os.environ.get('VFLV_SERVER_HOST', 'localhost')
    SECRET_KEY = os.environ.get('VFLV_SECRET_KEY', 
        '\xed\x8ege\xea}\x03\xc0\x8c$$\x98\xa4N\xa8\xb6\xf0k\x8a\x86\xe4\xa9\x19\xb7\x8a$')

    app.debug = DEBUG
    app.secret_key = SECRET_KEY
    print(' * Starting the server')
    app.run(host=HOST, port=PORT)
