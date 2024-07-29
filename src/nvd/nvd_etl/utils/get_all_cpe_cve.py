import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import pandas as pd
import ssl

# Load API key from .env file
load_dotenv()
NVD_API_KEY = os.getenv('NVD_API_KEY')

if not NVD_API_KEY:
    print("API key not found. Please ensure it is set in the .env file.")
    exit(1)

# Define the base URLs for the NVD API
BASE_URL_CVE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
BASE_URL_CPE = "https://services.nvd.nist.gov/rest/json/cpes/2.0"

# Create an SSL context that does not verify SSL certificates
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def fetch_data(session, url, start_index=0, results_per_page=2000):
    headers = {
        'apiKey': NVD_API_KEY
    }
    params = {
        'startIndex': start_index,
        'resultsPerPage': results_per_page
    }

    async with session.get(url, headers=headers, params=params, ssl=ssl_context) as response:
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Response status code: {response.status}")
        json_response = await response.json()
        return json_response


async def extract_cve_data():
    start_index = 0
    results_per_page = 2000
    all_cve_items = []

    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Fetching CVE data starting at index {start_index}")
            data = await fetch_data(session, BASE_URL_CVE, start_index, results_per_page)
            if data is None:
                break

            vulnerabilities = data.get('vulnerabilities', [])
            for vuln in vulnerabilities:
                cve_item = vuln.get('cve', {})
                cve_id = cve_item.get('id', 'N/A')
                published_date = cve_item.get('published', 'N/A')
                last_modified_date = cve_item.get('lastModified', 'N/A')
                descriptions = cve_item.get('descriptions', [])
                description = next((desc.get('value') for desc in descriptions if desc.get('lang') == 'en'), 'N/A')

                all_cve_items.append({
                    'CVE ID': cve_id,
                    'Published Date': published_date,
                    'Last Modified Date': last_modified_date,
                    'Description': description
                })

            total_results = data.get('totalResults', 0)
            if start_index + results_per_page >= total_results:
                break

            start_index += results_per_page
            await asyncio.sleep(6)  # Respect NVD API rate limits

    return all_cve_items


async def extract_cpe_data():
    start_index = 0
    results_per_page = 2000
    all_cpe_items = []

    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Fetching CPE data starting at index {start_index}")
            data = await fetch_data(session, BASE_URL_CPE, start_index, results_per_page)
            if data is None:
                break

            products = data.get('products', [])
            for product in products:
                cpe_item = product.get('cpe', {})
                cpe_name = cpe_item.get('cpeName', 'N/A')
                cpe_name_id = cpe_item.get('cpeNameId', 'N/A')
                deprecated = cpe_item.get('deprecated', False)
                created = cpe_item.get('created', 'N/A')
                last_modified = cpe_item.get('lastModified', 'N/A')
                titles = cpe_item.get('titles', [])
                title = next((title.get('title') for title in titles if title.get('lang') == 'en'), 'N/A')

                all_cpe_items.append({
                    'CPE Name': cpe_name,
                    'CPE Name ID': cpe_name_id,
                    'Deprecated': deprecated,
                    'Created Date': created,
                    'Last Modified Date': last_modified,
                    'Title': title
                })

            total_results = data.get('totalResults', 0)
            if start_index + results_per_page >= total_results:
                break

            start_index += results_per_page
            await asyncio.sleep(6)  # Respect NVD API rate limits

    return all_cpe_items


def save_data_to_csv(data_items, output_file):
    df = pd.DataFrame(data_items)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")


async def main():
    cve_items = await extract_cve_data()
    if not cve_items:
        print("No CVE data fetched.")
        return
    cpe_items = await extract_cpe_data()
    if not cpe_items:
        print("No CPE data fetched.")
        return

    output_dir = '../../nvd_data'
    os.makedirs(output_dir, exist_ok=True)
    save_data_to_csv(cve_items, os.path.join(output_dir, 'nvd_cve_data.csv'))
    save_data_to_csv(cpe_items, os.path.join(output_dir, 'nvd_cpe_data.csv'))


if __name__ == "__main__":
    asyncio.run(main())
