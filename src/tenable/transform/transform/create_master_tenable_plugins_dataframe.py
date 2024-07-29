import csv
import os

# Directory paths
input_dir = '../tenable_data/parsed_xml_files'
output_dir = '../tenable_data/master'
os.makedirs(output_dir, exist_ok=True)

# Initialize a dictionary to store rows by PluginId
data_by_plugin_id = {}

# Loop through each CSV file in the input directory
for csv_filename in os.listdir(input_dir):
    if csv_filename.endswith('.csv'):
        csv_file_path = os.path.join(input_dir, csv_filename)
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plugin_id = row['PluginId']
                if plugin_id not in data_by_plugin_id:
                    data_by_plugin_id[plugin_id] = row
                else:
                    # Merge rows with the same PluginId
                    for key, value in row.items():
                        if value and not data_by_plugin_id[plugin_id][key]:
                            data_by_plugin_id[plugin_id][key] = value

# Sort the data by PluginId in descending order
sorted_data = sorted(data_by_plugin_id.values(), key=lambda x: int(x['PluginId']), reverse=True)

# Write the combined data to a new CSV file in the output directory
output_file_path = os.path.join(output_dir, 'master.csv')
with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['PluginId', 'SourceFile', 'Title', 'Link', 'PublicationDate', 'Product', 'Severity', 'Synopsis', 'Description', 'Solution', 'CVEID']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in sorted_data:
        writer.writerow(row)

print(f'Combined CSV file created at {output_file_path}')