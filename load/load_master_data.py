import pandas as pd
import sqlite3
from pathlib2 import Path

# Database path
db_path = Path("../Tenable.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

# CSV file path
csv_file_path = Path("../tenable_data/master/master.csv")
csv_file_path.parent.mkdir(parents=True, exist_ok=True)

# Create and connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define the table creation SQL
table_name = "TenablePluginData"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    PluginId TEXT PRIMARY KEY,
    SourceFile TEXT,
    Title TEXT,
    Link TEXT,
    PublicationDate TEXT,
    Product TEXT,
    Severity TEXT,
    Synopsis TEXT,
    Description TEXT,
    Solution TEXT,
    CVEID TEXT
);
"""

# Create the table
cursor.execute(create_table_sql)

# Check if the CSV file exists
if not csv_file_path.exists():
    raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

# Load data from CSV
df = pd.read_csv(csv_file_path)

# Insert the data into the database
df.to_sql(table_name, conn, if_exists='append', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data from CSV inserted into the database.")