import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.types import String, DateTime, Float, Text
from pathlib2 import Path
from dotenv import load_dotenv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Define the database name and CSV file path
DATABASE_NAME = 'NVDb.db'
CSV_FILE = Path(__file__).resolve().parent.parent.parent / '../data/nvd_data/nvd_data.csv'

# Create a connection to the SQLite3 database using SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
metadata = MetaData()

# Load the data from the CSV file into a pandas DataFrame
csv_path = Path(CSV_FILE)
df = pd.read_csv(csv_path, dtype=str, quotechar='"', escapechar='\\', on_bad_lines='skip')
logging.info(f"Data loaded from '{csv_path}' into DataFrame.")
logging.info(f"First few rows of the DataFrame:\n{df.head()}")

# Sanitize column names
sanitized_columns = {col: re.sub(r'\W|^(?=\d)', '_', col) for col in df.columns}
df.rename(columns=sanitized_columns, inplace=True)
logging.info(f"Sanitized columns: {sanitized_columns}")

# Define the nvd_data table using sanitized column names
columns = [Column(col, String) for col in df.columns]
nvd_data_table = Table('nvd_data', metadata, *columns)

# Create the table in the database
metadata.create_all(engine)
logging.info(f"Table 'nvd_data' created in the database '{DATABASE_NAME}' with columns: {df.columns.tolist()}")

# Convert date columns to datetime and then to string
date_columns = ['Published_Date', 'Last_Modified_Date', 'CISA_Exploit_Add', 'CISA_Action_Due']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

# Convert DataFrame to list of dictionaries
data = df.to_dict(orient='records')
logging.info(f"First few records to be inserted:\n{data[:5]}")

# Insert data into the nvd_data table using SQLAlchemy bulk insert
with engine.connect() as conn:
    conn.execute(insert(nvd_data_table), data)
    logging.info(f"Data from '{csv_path}' has been successfully inserted into the '{DATABASE_NAME}' database.")