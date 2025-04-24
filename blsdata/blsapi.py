import csv
import time
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# config

series_df = pd.read_csv("blsdata/series_ids.csv")
SERIES_IDS = series_df["Series ID"].tolist()

START_YEAR = "1997"
END_YEAR = "2023"
OUTPUT_FILE = "median_wages_by_state.csv"

API_KEY = os.getenv("BLS_API_KEY")

# api request

def fetch_bls_data(series_ids, startyear, endyear):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    payload = {
        "seriesid": series_ids,
        "startyear": startyear,
        "endyear": endyear
    }

    if API_KEY:
        payload["registrationkey"] = API_KEY

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"BLS API error: {response.status_code}, {response.text}")

    return response.json()

# data extraction

def parse_bls_response(json_data, series_df):
    all_rows = []

    id_to_state = dict(zip(series_df["Series ID"], series_df["State"]))

    for series in json_data["Results"]["series"]:
        series_id = series['seriesID']
        state = id_to_state.get(series_id, "Unknown")
        
        for entry in series['data']:
            year = entry['year']
            period = entry['period']
            if period.startswith('M'):
                month = period[1:]
                value = entry['value']
                all_rows.append({
                    "series_id": series_id,
                    "state": state,
                    "year": int(year),
                    "month": int(month),
                    "value": float(value)
                })

    return all_rows


# write to csv

def save_to_csv(rows, filename):
    if not rows:
        print("No Data to Save")
        return
    keys = rows[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


# main

if __name__ == "__main__":
    print(f"Fetching data for {len(SERIES_IDS)} series...")
    data = fetch_bls_data(SERIES_IDS, START_YEAR, END_YEAR)
    parsed = parse_bls_response(data, series_df)
    save_to_csv(parsed, OUTPUT_FILE)
    print(f"Saved {len(parsed)} records to {OUTPUT_FILE}")
    raw = fetch_bls_data(SERIES_IDS, START_YEAR, END_YEAR)
    # print(json.dumps(raw, indent=2))  

