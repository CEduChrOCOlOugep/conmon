import xml.etree.ElementTree as ET
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import sqlite3

# Directory paths
input_dir = "../tenable_data/xml_files"
db_path = "/Users/brandynlacourse/conmon/db/NVD.db"

# Create and connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def sanitize_table_name(name):
    """ Sanitize the XML file name to create a valid SQLite table name. """
    return re.sub(r'[^a-zA-Z0-9]', '', name).upper()


def parse_xml_to_db(xml_file, cursor):
    """ Parse XML file and insert data into the SQLite database. """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Table name is now constant
    table_name = "MasterTenablePlugins"

    # Create table if it doesn't exist
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        "index" INTEGER,
        pluginId TEXT PRIMARY KEY,
        sourceFile TEXT,
        title TEXT,
        link TEXT,
        publicationDate TEXT,
        product TEXT,
        severity TEXT,
        synopsis TEXT,
        description TEXT,
        solution TEXT,
        cve TEXT
    );
    """)

    # Insert data into table
    index = 0
    for item in root.findall('.//item'):
        plugin_id_text = item.find('description').text.strip().lower() if item.find(
            'description') is not None else ''
        plugin_id_match = re.search(r'plugin id (\d+)', plugin_id_text)
        plugin_id = plugin_id_match.group(1).lower() if plugin_id_match else None

        if plugin_id:
            data = [
                index,
                plugin_id,
                os.path.basename(xml_file),
                item.findtext('title', '').strip().lower(),
                item.findtext('link', '').strip().lower(),
                item.findtext('pubDate', '').strip().lower(),
                '',  # Placeholder for product
                '',  # Placeholder for severity
                '',  # Placeholder for synopsis
                BeautifulSoup(item.findtext('description', ''), 'html.parser').get_text(strip=True).lower(),
                '',  # Placeholder for solution
                ''  # Placeholder for CVE
            ]

            cursor.execute(
                f"INSERT INTO {table_name} (\"index\", pluginId, sourceFile, title, link, publicationDate, product, severity, synopsis, description, solution, cve) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                tuple(data))
            index += 1


# Parse XML files and insert data into database
for xml_filename in os.listdir(input_dir):
    if xml_filename.endswith('.xml'):
        xml_file_path = os.path.join(input_dir, xml_filename)
        parse_xml_to_db(xml_file_path, cursor)

conn.commit()
conn.close()
print("Data inserted into the database.")
