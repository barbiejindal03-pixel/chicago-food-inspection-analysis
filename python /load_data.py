Chicago Food Inspection — Data Loading Script 

WHY THIS EXISTS:
    DBeaver ran out of memory trying to import 308,357 rows directly from CSV.
    This Python script uses the built-in csv and sqlite3 libraries to load the
    dataset into a local SQLite database — no extra installs needed.

HOW TO USE:
    1. Download the dataset from the Chicago Open Data Portal:
       https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4dn7-eekw
    2. Save the CSV file to your Desktop
    3. Open Terminal and run:
           python3 load_data.py
    4. Open the .db file in DBeaver or DB Browser for SQLite
    5. Run the queries in sql/queries.sql

import sqlite3
import csv

CSV_PATH = "/Users/barbiejindal/Desktop/chicago food project/Food_Inspections_20260408.csv"
DB_PATH  = "/Users/barbiejindal/Desktop/chicago food project/chicago_food.db"

def load_data():
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # Create the inspections table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            inspection_id   TEXT,
            dba_name        TEXT,
            aka_name        TEXT,
            license_num     TEXT,
            facility_type   TEXT,
            risk            TEXT,
            address         TEXT,
            city            TEXT,
            state           TEXT,
            zip             TEXT,
            inspection_date TEXT,
            inspection_type TEXT,
            results         TEXT,
            violations      TEXT,
            latitude        TEXT,
            longitude       TEXT
        )
    """)
    print("Table created.")

    # Load CSV rows into the table
    print(f"Loading CSV from: {CSV_PATH}")
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO inspections VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    row.get("Inspection ID",   ""),
                    row.get("DBA Name",        ""),
                    row.get("AKA Name",        ""),
                    row.get("License #",       ""),
                    row.get("Facility Type",   ""),
                    row.get("Risk",            ""),
                    row.get("Address",         ""),
                    row.get("City",            ""),
                    row.get("State",           ""),
                    row.get("Zip",             ""),
                    row.get("Inspection Date", ""),
                    row.get("Inspection Type", ""),
                    row.get("Results",         ""),
                    row.get("Violations",      ""),
                    row.get("Latitude",        ""),
                    row.get("Longitude",       ""),
                )
            )

    conn.commit()
    conn.close()
    print("Done! All rows loaded into:", DB_PATH)
    print("Open the .db file in DBeaver and run: SELECT COUNT(*) FROM inspections;")


if __name__ == "__main__":
    load_data()
