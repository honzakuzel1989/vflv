"""
Verificators tests
"""

import re
import unittest
import verificators as x

class VerificatorsTest(unittest.TestCase):
    def test_verify_bad_password(self):
        # delka alespon 4
        ret, _ = x.verify_password('')
        self.assertEqual(ret, False)
        ret, _ = x.verify_password('1k')
        self.assertEqual(ret, False)
        
        # jedno pismeno
        ret, _ = x.verify_password('12345')
        self.assertEqual(ret, False)
        
        # jedno cislo
        ret, _ = x.verify_password('qwerty')
        self.assertEqual(ret, False)

    def test_verify_good_password(self):
        ret, _ = x.verify_password('qwert1')
        self.assertEqual(ret, True)
        
        ret, _ = x.verify_password('12345a')
        self.assertEqual(ret, True)

    def test_verify_bad_voting_values(self):
        # min 1 hodnoty
        ret, _ = x.verify_voting_values([])
        self.assertEqual(ret, False)
        
        # max 3 hodnoty
        ret, _ = x.verify_voting_values([1,1,1,1,1,1])
        self.assertEqual(ret, False)
        
        # maximalni hodnota 3
        ret, _ = x.verify_voting_values([5])
        self.assertEqual(ret, False)
        
        # unikatni hodnota
        ret, _ = x.verify_voting_values([2,3,2])
        self.assertEqual(ret, False)
        
        ret, _ = x.verify_voting_values(['2','3',2])
        self.assertEqual(ret, False)
        
        # konvertovatelne na int
        ret, _ = x.verify_voting_values(['hello','3',2])
        self.assertEqual(ret, False)

    def test_verify_good_voting_values(self):
        ret, _ = x.verify_voting_values([1, 2, 3])
        self.assertEqual(ret, True)
        
        ret, _ = x.verify_voting_values([2, 3, 1])
        self.assertEqual(ret, True)
        
        for i in [1, 2, 3]:
            ret, _ = x.verify_voting_values([i])
            self.assertEqual(ret, True)
        
        ret, _ = x.verify_voting_values([1, 2])
        self.assertEqual(ret, True)
        
        ret, _ = x.verify_voting_values([3, 2])
        self.assertEqual(ret, True)
        
        ret, _ = x.verify_voting_values([1, 3])
        self.assertEqual(ret, True)

if __name__ == '__main__':
    unittest.main()
