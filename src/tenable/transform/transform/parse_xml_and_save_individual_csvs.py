import csv
import xml.etree.ElementTree as ET
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

# Directory paths
input_dir = '../tenable_data/xml_files'
output_dir = '../tenable_data/parsed_xml_files'
os.makedirs(output_dir, exist_ok=True)


# Function to clean text by removing double quotes and colons
def clean_text(text):
    return text.replace('"', '').replace(':', '')


# Function to parse XML and write to CSV
def parse_xml_to_csv(xml_file, csv_file):
    # Load and parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open a CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(
            ['PluginId', 'SourceFile', 'Title', 'Link', 'PublicationDate', 'Product', 'Severity', 'Synopsis',
             'Description', 'Solution', 'CVEID'])

        # Iterate through each item in the XML
        for item in root.findall('.//item'):
            title = clean_text(item.find('title').text.strip().lower() if item.find('title') is not None else '')
            link = clean_text(item.find('link').text.strip().lower() if item.find('link') is not None else '')
            pub_date = clean_text(item.find('pubDate').text.strip().lower() if item.find('pubDate') is not None else '')
            description_html = clean_text(
                item.find('description').text.strip().lower() if item.find('description') is not None else '')

            # Parse HTML content within description using BeautifulSoup
            soup = BeautifulSoup(description_html, 'html.parser')
            plugin_id_text = clean_text(soup.find('p').get_text(strip=True).lower() if soup.find('p') else '')
            severity = clean_text(
                plugin_id_text.split('severity')[0].split()[-1] if 'severity' in plugin_id_text else '')
            synopsis = clean_text(
                soup.find('h3', string='synopsis').find_next_sibling('span').get_text(strip=True).lower() if soup.find(
                    'h3', string='synopsis') else '')
            description_text = clean_text(soup.find('h3', string='description').find_next_sibling('span').get_text(
                strip=True).lower() if soup.find('h3', string='description') else '')
            solution = clean_text(
                soup.find('h3', string='solution').find_next_sibling('span').get_text(strip=True).lower() if soup.find(
                    'h3', string='solution') else '')

            # Extract CVE from the description
            cve_match = re.search(r'cve-\d{4}-\d{4,7}', description_html)
            cve = clean_text(cve_match.group(0).lower() if cve_match else '')

            # Extract Plugin ID and Product from the plugin_id_text
            plugin_id_match = re.search(r'plugin id (\d+)', plugin_id_text)
            plugin_id = clean_text(plugin_id_match.group(1).lower() if plugin_id_match else '')
            product_match = re.match(r'(.*) plugin id \d+', plugin_id_text)
            product = clean_text(product_match.group(1).strip().lower() if product_match else '')

            # Convert publication date to a standard date format
            try:
                pub_date_parsed = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                pub_date_formatted = pub_date_parsed.strftime('%Y-%m-%d')
            except Exception as e:
                pub_date_formatted = pub_date

            # Write the extracted data to the CSV file
            writer.writerow(
                [plugin_id, os.path.relpath(xml_file, start=os.path.dirname(input_dir)), title, link,
                 pub_date_formatted, product, severity, synopsis, description_text,
                 solution, cve])


# Loop through each XML file in the input directory
for xml_filename in os.listdir(input_dir):
    if xml_filename.endswith('.xml'):
        xml_file_path = os.path.join(input_dir, xml_filename)
        csv_filename = f'parsed_{os.path.splitext(xml_filename)[0]}.csv'
        csv_file_path = os.path.join(output_dir, csv_filename)
        parse_xml_to_csv(xml_file_path, csv_file_path)
        print(f'Parsed {xml_file_path} to {csv_file_path}')
