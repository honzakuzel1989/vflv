"""
Helpers tests
"""

import unittest
import helpers as x

from datetime import datetime

class HelpersTest(unittest.TestCase):
    def test_compute_hash_in_hex(self):
        self.assertEqual(x.compute_hash_in_hex('kuz1'),
            '79887b3f8596d73cd7bc44cc00543f466cf3d2ccf180ca8d2046c053673ee7b4')
        self.assertEqual(x.compute_hash_in_hex('kli1'),
            '2d3bcb537ec2891aceb338f1d6ca08953aea6d85b4cc9ef4706f9a21c828c42c')
        self.assertEqual(x.compute_hash_in_hex('mar5'),
            'b5aeaf6e2dec5352a77430c11a61aaeedc42d3b1e5624423a62daedacbcef6f5')
        self.assertEqual(x.compute_hash_in_hex('kor1'),
            '47579f662fc3d7cd6bdf78cdb6e44a17a20c46045bd188a1da05cbcaf27c73ce')
        self.assertEqual(x.compute_hash_in_hex('dyc1'),
            '37450720bfa246a4fc703953366131d4ac2af393161986d459d8603e2729321e')

    def test_get_current_time_in_s(self):
        self.assertEqual(x.get_time_in_s(datetime(2015,3,20)), 1426809600)
        self.assertEqual(x.get_time_in_s(datetime(1970,1,1)), 0)
        self.assertEqual(x.get_time_in_s(datetime(1999,9,9)), 936835200)
        self.assertEqual(x.get_time_in_s(datetime(2050,5,5)), 2535321600)
        self.assertEqual(x.get_time_in_s(datetime(2015,7,17)) - x.get_time_in_s(datetime(2015,7,16)), 60*60*24)

if __name__ == '__main__':
    unittest.main()
