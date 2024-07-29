import os
import json
import pandas as pd

# Define the directory containing the JSON schema files
schema_dir = '/Users/brandynlacourse/VSCodeProjects/nvd_etl/reference/schemas'

# List to hold the extracted data
data = []

# Iterate through all files in the directory
for filename in os.listdir(schema_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(schema_dir, filename)
        with open(file_path, 'r') as file:
            schema = json.load(file)
            # Extract fields from the properties object
            for key, value in schema.get('properties', {}).items():
                data.append({
                    'source_file': filename,
                    'key': key,
                    'value': value
                })

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_csv = 'extracted_fields.csv'
df.to_csv(output_csv, index=False)

print(f"Data has been successfully extracted and saved to {output_csv}")