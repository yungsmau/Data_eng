import sqlite3
import pandas as pd
from glob import glob
import os


conn = sqlite3.connect("05/crime_data.db")
cursor = conn.cursor()

csv_files = glob("05/**/*.csv", recursive=True)

for file_path in csv_files:
    folder_name = os.path.basename(os.path.dirname(file_path))
    table_name = folder_name.replace(" ", "_").lower()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        crime_id TEXT UNIQUE,
        month TEXT NOT NULL,
        reported_by TEXT NOT NULL,
        falls_within TEXT NOT NULL,
        longitude REAL,
        latitude REAL,
        location TEXT,
        lsoa_code TEXT,
        lsoa_name TEXT,
        crime_type TEXT,
        last_outcome_category TEXT
    );
    """

    cursor.execute(create_table_query)
    data = pd.read_csv(file_path)
    data = pd.DataFrame(data)

    for index, row in data.iterrows():
        insert_query = f"""
        INSERT OR REPLACE INTO {table_name} (crime_id, month, reported_by, falls_within, longitude, latitude, location, lsoa_code, lsoa_name, crime_type, last_outcome_category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        cursor.execute(
            insert_query,
            (
                row["Crime ID"],
                row["Month"],
                row["Reported by"],
                row["Falls within"],
                row["Longitude"],
                row["Latitude"],
                row["Location"],
                row["LSOA code"],
                row["LSOA name"],
                row["Crime type"],
                row["Last outcome category"],
            ),
        )

conn.commit()
conn.close()
