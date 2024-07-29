import requests
import os

# List of URLs with their corresponding file names
urls = {
    "newest_plugins": "https://www.tenable.com/plugins/feeds?sort=newest",
    "updated_plugins": "https://www.tenable.com/plugins/feeds?sort=updated",
    "newest_nessus_plugins": "https://www.tenable.com/plugins/feeds?sort=updated&type=nessus",
    "updated_nessus_plugins": "https://www.tenable.com/plugins/feeds?sort=updated&type=nessus",
    "newest_web_app_scanning_plugins": "https://www.tenable.com/plugins/feeds?sort=newest&type=was",
    "updated_web_app_scanning_plugins": "https://www.tenable.com/plugins/feeds?sort=updated&type=was",
    "newest_nessus_network_monitor_plugins": "https://www.tenable.com/plugins/feeds?sort=newest&type=nnm",
    "updated_nessus_network_monitor_plugins": "https://www.tenable.com/plugins/feeds?sort=updated&type=nnm",
    "newest_log_correlation_engine_plugins": "https://www.tenable.com/plugins/feeds?sort=newest&type=lce",
    "updated_log_correlation_engine_plugins": "https://www.tenable.com/plugins/feeds?sort=updated&type=lce"
}

# Directory to save the XML files
output_dir = "../tenable_data/xml_files"
os.makedirs(output_dir, exist_ok=True)

# Loop through each URL and save the XML data to a file
for name, url in urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(output_dir, f"{name}.xml")
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Saved XML data to {file_path}")
    else:
        print(f"Failed to fetch data from {url}")