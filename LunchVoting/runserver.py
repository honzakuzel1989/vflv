# -*- coding: ISO-8859-2 -*-
"""
This script runs the LunchVoting application using a development server.
"""

import os

from os import environ
from LunchVoting import app

if __name__ == '__main__':
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'vflv.db'),
    ))

    HOST = environ.get('SERVER_HOST', 'localhost')
    PORT = int(environ.get('SERVER_PORT', '5555'))

    app.secret_key = '\xed\x8e\xea}\x03\xc0\x8c$$\x98\xa4\
        N\xa8\xb6\xf0k\x8a\x86\xe4\xa9\x19\xb7\x8a$'
    app.run(host=HOST, port=PORT, debug=True)
    print('Started the server.')
    
