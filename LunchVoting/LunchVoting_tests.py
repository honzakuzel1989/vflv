import os
import unittest
import tempfile
import LunchVoting

class LunchVotingTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, LunchVoting.app.config['DATABASE'] = tempfile.mkstemp()
        LunchVoting.app.config['TESTING'] = True
        self.app = LunchVoting.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(LunchVoting.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
