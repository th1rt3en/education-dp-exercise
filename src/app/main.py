import pandas as pd

from pymongo import DESCENDING
from fastapi import FastAPI, UploadFile, File, BackgroundTasks

from app.utils import parse_data, enrich_data
from app.db import (
    annual_university,
    latest_university,
    top_university
)

app = FastAPI()


def update_latest_university():
    """
    Find latest data for each university and update `latest_university` collection
    :return:
    """
    for university in annual_university.distinct("Institution"):
        latest_data = annual_university.find_one({"Institution": university}, sort=[("year", DESCENDING)])
        latest_university.replace_one({"Institution": university}, latest_data, upsert=True)


def update_top_university():
    """
    Find top university for each country and update `top_university` collection
    :return:
    """
    for country in latest_university.distinct("Location"):
        best_university = latest_university.find_one({"Location": country}, sort=[("Alumni Employment", DESCENDING)])
        top_university.replace_one({"Location": country}, best_university, upsert=True)


@app.put("/submit/{year}", status_code=201)
def submit(year, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file, sep="\t")
        df = parse_data(df)
        # Remove whitespace from both ends of column names
        created = 0
        updated = 0
        for idx, row in df.iterrows():
            data = row.to_dict()
            # Set year column
            data["year"] = year
            data = enrich_data(data)
            # Upsert data
            result = annual_university.replace_one({"Institution": data["Institution"], "year": year}, data, upsert=True)
            # Increment created and updated counter
            created += 1 - result.modified_count
            updated += result.modified_count

        # Start background tasks to update other collections
        background_tasks.add_task(update_latest_university)
        background_tasks.add_task(update_top_university)

        return {"msg": "Successful", "data": {"rows_created": created, "rows_updated": updated}}
    except Exception as e:
        print(e)
        return {"error": str(e)}
