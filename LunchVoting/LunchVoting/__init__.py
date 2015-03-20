"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.secret_key = '\xed\x8e\xea}\x03\xc0\x8c$$\x98\xa4\
        N\xa8\xb6\xf0k\x8a\x86\xe4\xa9\x19\xb7\x8a$'

import LunchVoting.views
