import unittest
import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standalone'))
from calculate_revenue import calculate_total_revenue

class TestRevenueCalculation(unittest.TestCase):
    def setUp(self):
        self.test_file = 'tests/data_sample.csv'
        with open(self.test_file, 'w', newline='') as f:
            f.write("id_client,chiffre_affaires\nC1,100.50\nC2,200.00\nC3,50.25")

    def test_calculate_total_revenue(self):
        result = calculate_total_revenue(self.test_file)
        self.assertEqual(result, 350.75)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
