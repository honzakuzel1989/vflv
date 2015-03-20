# -*- coding: ISO-8859-2 -*-
"""
This script runs the LunchVoting application using a development server.
"""

import os
from LunchVoting import app

if __name__ == '__main__':
    DEBUG = int(os.environ.get('DEBUG', '0'))
    PORT = int(os.environ.get('SERVER_PORT', '5555'))

    if DEBUG:
        app.debug = True
        HOST = os.environ.get('SERVER_HOST', 'localhost')
    else:
        HOST = '0.0.0.0'

    app.run(host=HOST, port=PORT)
    print('Started the server.')
