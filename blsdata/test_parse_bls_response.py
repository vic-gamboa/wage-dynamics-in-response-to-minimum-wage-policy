import unittest
import pandas as pd
from blsapi import parse_bls_response  

class TestParseBLSResponse(unittest.TestCase):

    def setUp(self):
        self.series_df = pd.DataFrame({
            "Series ID": ["SERIES001"],
            "State": ["California"]
        })

        self.sample_json = {
            "Results": {
                "series": [
                    {
                        "seriesID": "SERIES001",
                        "data": [
                            {"year": "2020", "period": "M05", "value": "25.50"},
                            {"year": "2020", "period": "A01", "value": "27.00"},  
                        ]
                    }
                ]
            }
        }

    def test_basic_parsing(self):
        result = parse_bls_response(self.sample_json, self.series_df)
        self.assertEqual(len(result), 1)  # only the M05 row should be kept
        row = result[0]
        self.assertEqual(row["series_id"], "SERIES001")
        self.assertEqual(row["state"], "California")
        self.assertEqual(row["year"], 2020)
        self.assertEqual(row["month"], 5)
        self.assertEqual(row["value"], 25.50)

    def test_unknown_series_id(self):
        # Change the series ID so it's not in the mapping
        unknown_json = {
            "Results": {
                "series": [
                    {
                        "seriesID": "UNKNOWN001",
                        "data": [{"year": "2021", "period": "M01", "value": "30.00"}]
                    }
                ]
            }
        }
        result = parse_bls_response(unknown_json, self.series_df)
        self.assertEqual(result[0]["state"], "Unknown")

    def test_empty_series(self):
        empty_json = {"Results": {"series": []}}
        result = parse_bls_response(empty_json, self.series_df)
        self.assertEqual(result, [])

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=["Series ID", "State"])
        result = parse_bls_response(self.sample_json, empty_df)
        self.assertEqual(result[0]["state"], "Unknown")

    def test_empty_but_valid_response(self):
        json_data = {
        "Results": {
            "series": [
                {
                    "seriesID": "SERIES001",
                    "data": [
                        {"year": "2022", "period": "A01", "value": "30.0"}  # Should be filtered out
                    ]
                }
            ]
        }
    }
        series_df = pd.DataFrame({
            "Series ID": ["SERIES001"],
            "State": ["California"]
        })

        result = parse_bls_response(json_data, series_df)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()

