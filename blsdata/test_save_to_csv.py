import unittest
import os
import csv
from blsapi import save_to_csv  

class TestSaveToCSV(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_output.csv"
        self.test_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]

    def test_csv_creation_and_content(self):
        save_to_csv(self.test_data, self.test_file)

        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            self.assertEqual(len(rows), 2)

            self.assertEqual(rows[0]['name'], "Alice")
            self.assertEqual(int(rows[0]['age']), 30)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()

