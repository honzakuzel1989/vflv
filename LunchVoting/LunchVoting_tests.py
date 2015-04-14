import os
import unittest
import tempfile
import LunchVoting

class LunchVotingTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, LunchVoting.app.config['DATABASE'] = tempfile.mkstemp()
        LunchVoting.app.config['TESTING'] = True
        LunchVoting.app.config['SECRET_KEY'] = 'testing secret key'
        self.app = LunchVoting.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(LunchVoting.app.config['DATABASE'])

    def __login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def __logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_logio(self):
        rv = self.__login('', '')
        assert 'Invalid username.' in rv.data
        rv = self.__login('pri1', '')
        assert 'Invalid username.' in rv.data
        rv = self.__login('kuz1', '')
        assert 'Invalid password.' in rv.data
        rv = self.__login('kuz1', 'pri1')
        assert 'Invalid password.' in rv.data
        rv = self.__login('kuz1', 'kuz1')
        assert 'Voting.' in rv.data

if __name__ == '__main__':
    unittest.main()
