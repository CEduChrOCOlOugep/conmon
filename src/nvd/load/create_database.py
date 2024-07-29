import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, MetaData, Float, Boolean, Text, DateTime, Date
from sqlalchemy.dialects.sqlite import insert
from pathlib2 import Path
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Define the database name and CSV file path
DATABASE_NAME = 'NVDb.db'
CSV_FILE = Path(__file__).parent / 'data/nvd_data/nvd_data.csv'

# Create a connection to the SQLite3 database using SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
metadata = MetaData()

# Define the nvd_data table using column names and data types from the API schema
nvd_data_table = Table('nvd_data', metadata,
    Column('cve_id', String),
    Column('sourceIdentifier', String),
    Column('vulnStatus', String),
    Column('published', DateTime),
    Column('lastModified', DateTime),
    Column('evaluatorComment', Text),
    Column('evaluatorSolution', Text),
    Column('evaluatorImpact', Text),
    Column('cisaExploitAdd', Date),
    Column('cisaActionDue', Date),
    Column('cisaRequiredAction', Text),
    Column('cisaVulnerabilityName', String),
    Column('cveTags', Text),
    Column('descriptions', Text),
    Column('references', Text),
    Column('cvssMetricV31_version', String),
    Column('cvssMetricV31_vectorString', String),
    Column('cvssMetricV31_attackVector', String),
    Column('cvssMetricV31_attackComplexity', String),
    Column('cvssMetricV31_privilegesRequired', String),
    Column('cvssMetricV31_userInteraction', String),
    Column('cvssMetricV31_scope', String),
    Column('cvssMetricV31_confidentialityImpact', String),
    Column('cvssMetricV31_integrityImpact', String),
    Column('cvssMetricV31_availabilityImpact', String),
    Column('cvssMetricV31_baseScore', Float),
    Column('cvssMetricV31_baseSeverity', String),
    Column('cvssMetricV31_exploitCodeMaturity', String),
    Column('cvssMetricV31_remediationLevel', String),
    Column('cvssMetricV31_reportConfidence', String),
    Column('cvssMetricV31_temporalScore', Float),
    Column('cvssMetricV31_temporalSeverity', String),
    Column('cvssMetricV31_confidentialityRequirement', String),
    Column('cvssMetricV31_integrityRequirement', String),
    Column('cvssMetricV31_availabilityRequirement', String),
    Column('cvssMetricV31_modifiedAttackVector', String),
    Column('cvssMetricV31_modifiedAttackComplexity', String),
    Column('cvssMetricV31_modifiedPrivilegesRequired', String),
    Column('cvssMetricV31_modifiedUserInteraction', String),
    Column('cvssMetricV31_modifiedScope', String),
    Column('cvssMetricV31_modifiedConfidentialityImpact', String),
    Column('cvssMetricV31_modifiedIntegrityImpact', String),
    Column('cvssMetricV31_modifiedAvailabilityImpact', String),
    Column('cvssMetricV31_environmentalScore', Float),
    Column('cvssMetricV31_environmentalSeverity', String)
)

# Create the table in the database
metadata.create_all(engine)
logging.info(f"Table 'nvd_data' created in the database '{DATABASE_NAME}'.")

# Load the data from the CSV file into a pandas DataFrame
csv_path = Path(CSV_FILE)
df = pd.read_csv(csv_path, dtype=str)
logging.info(f"Data loaded from '{csv_path}' into DataFrame.")

# Convert date columns to datetime
date_columns = ['published', 'lastModified', 'cisaExploitAdd', 'cisaActionDue']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Convert DataFrame to list of dictionaries
data = df.to_dict(orient='records')

# Insert data into the nvd_data table using SQLAlchemy bulk insert
with engine.connect() as conn:
    conn.execute(insert(nvd_data_table), data)
    logging.info(f"Data from '{csv_path}' has been successfully inserted into the '{DATABASE_NAME}' database.")