import requests

from typing import Dict
from pandas import DataFrame


def parse_data(df: DataFrame) -> DataFrame:
    # Remove whitespace at both ends of column name
    df.columns = df.columns.str.strip()
    try:
        df["Quality of Education"] = df["Quality of Education"].str.extract(r"(\d+)").fillna(0).astype("int")
        df["Quality of Faculty"] = df["Quality of Faculty"].str.extract(r"(\d+)").fillna(0).astype("int")
        df["Alumni Employment"] = df["Alumni Employment"].str.extract(r"(\d+)").fillna(0).astype("int")
        # Remove location from name
        df["Institution"] = df["Institution"].str.extract(r"([a-zA-Z ]+)(?:,.*)?")
    except KeyError:
        print("Missing column(s)")
    return df


def enrich_data(data: Dict) -> Dict:
    # May not work due to duckduckgo api rate limit?
    api_url = "https://api.duckduckgo.com/"
    params = {
        "q": data["Institution"],
        "format": "json"
    }
    try:
        extra_data = requests.get(api_url, params=params, timeout=1).json()
        data["url"] = extra_data.get("AbstractUrl")
        data["description"] = extra_data.get("AbstractText")
    except Exception:
        print("Failed to enrich data")
    return data
