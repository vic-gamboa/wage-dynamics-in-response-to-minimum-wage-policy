import unittest
from blsapi import fetch_bls_data

class TestFetchBLSData(unittest.TestCase):
    def test_valid_series(self):
        series_ids = ['CUUR0000SA0']
        result = fetch_bls_data(series_ids, "2022", "2022")

        self.assertIn("Results", result)
        self.assertIn("series", result["Results"])
        self.assertGreater(len(result["Results"]["series"]), 0)
        self.assertEqual(result["Results"]["series"][0]["seriesID"], "CUUR0000SA0")

    def test_invalid_series(self):
        series_ids = ['FAKE0000BAD']
        result = fetch_bls_data(series_ids, "2022", "2022")

        self.assertIn("Results", result)
        self.assertEqual(result["Results"]["series"][0]["seriesID"], "FAKE0000BAD")
        self.assertEqual(result["Results"]["series"][0]["data"], [])

    def test_time_range(self):
        series_ids = ['CUUR0000SA0']
        result = fetch_bls_data(series_ids, "2020", "2020")
        years = [int(entry["year"]) for entry in result["Results"]["series"][0]["data"]]
        self.assertTrue(all(y == 2020 for y in years))


if __name__ == "__main__":
    unittest.main()
