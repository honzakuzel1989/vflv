# -*- coding: ISO-8859-2 -*-
"""
This script runs the LunchVoting application using a development server.
"""

import os
from LunchVoting import app

if __name__ == '__main__':
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'vflv.db'),
    ))

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    PORT = int(os.environ.get('SERVER_PORT', '5555'))

    app.run(host=HOST, port=PORT, debug=True)
    print('Started the server.')
    
