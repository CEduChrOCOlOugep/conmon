from sqlalchemy import create_engine, Table, MetaData, select, func
from dotenv import load_dotenv
from pathlib2 import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Define the database name
DATABASE_NAME = 'NVDb.db'

# Create a connection to the SQLite3 database using SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
metadata = MetaData()

# Reflect the nvd_data table from the database
nvd_data_table = Table('nvd_data', metadata, autoload_with=engine)

# Create a select statement to query the top 10 records
stmt = select(nvd_data_table).limit(10)

# Execute the query and fetch the results
with engine.connect() as conn:
    result = conn.execute(stmt)
    rows = result.fetchall()
    if rows:
        logging.info(f"Top 10 records from 'nvd_data' table:")
        for row in rows:
            print(row)
    else:
        logging.info("No data found in 'nvd_data' table.")
        # Additional logging to debug
        count_stmt = select(func.count()).select_from(nvd_data_table)
        count_result = conn.execute(count_stmt)
        count = count_result.scalar()
        logging.info(f"Total number of records in 'nvd_data' table: {count}")