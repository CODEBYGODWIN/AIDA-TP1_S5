import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standalone'))
from categorize_clients import categorize_clients

class TestCat(unittest.TestCase):
    def test_cat(self):
        res = categorize_clients('tests/cat_sample.csv')
        self.assertEqual(res['Fidéliser'], 1)
        self.assertEqual(res['Relancer'], 1)
        self.assertEqual(res['Surveiller'], 1)

if __name__ == '__main__':
    unittest.main()