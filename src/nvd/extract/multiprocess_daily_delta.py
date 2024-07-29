import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import pandas as pd
import ssl
from datetime import datetime, timezone
from multiprocessing import Process, Queue
from pathlib import Path

# Load API key from .env file
load_dotenv()
NVD_API_KEY = os.getenv('NVD_API_KEY')

if not NVD_API_KEY:
    print("API key not found. Please ensure it is set in the .env file.")
    exit(1)

# Define the base URL for the NVD API
BASE_URL_CVE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Create an SSL context that does not verify SSL certificates
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

LAST_MODIFIED_FILE = 'nvd_daily_deltas.csv'


def read_last_modified_date():
    if os.path.exists(LAST_MODIFIED_FILE):
        df = pd.read_csv(LAST_MODIFIED_FILE)
        if not df.empty:
            return df['last_modified'].iloc[0]
    return None


def write_last_modified_date(last_modified):
    df = pd.DataFrame([{'last_modified': last_modified}])
    df.to_csv(LAST_MODIFIED_FILE, index=False)


async def fetch_data(session, url, params):
    headers = {
        'apiKey': NVD_API_KEY
    }

    async with session.get(url, headers=headers, params=params, ssl=ssl_context) as response:
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Response status code: {response.status}")
        json_response = await response.json()
        return json_response


async def extract_data(queue, base_url, params):
    start_index = 0
    results_per_page = 2000

    async with aiohttp.ClientSession() as session:
        while True:
            params.update({
                'startIndex': start_index,
                'resultsPerPage': results_per_page
            })

            print(f"Fetching CVE data starting at index {start_index}")
            data = await fetch_data(session, base_url, params)
            if not data:
                break

            items = data.get('vulnerabilities', [])
            for item in items:
                cve_item = item.get('cve', {})
                cve_id = cve_item.get('id', 'N/A')
                source_identifier = cve_item.get('sourceIdentifier', 'N/A')
                vuln_status = cve_item.get('vulnStatus', 'N/A')
                published_date = cve_item.get('published', 'N/A')
                last_modified_date = cve_item.get('lastModified', 'N/A')
                evaluator_comment = cve_item.get('evaluatorComment', 'N/A')
                evaluator_solution = cve_item.get('evaluatorSolution', 'N/A')
                evaluator_impact = cve_item.get('evaluatorImpact', 'N/A')
                cisa_exploit_add = cve_item.get('cisaExploitAdd', 'N/A')
                cisa_action_due = cve_item.get('cisaActionDue', 'N/A')
                cisa_required_action = cve_item.get('cisaRequiredAction', 'N/A')
                cisa_vulnerability_name = cve_item.get('cisaVulnerabilityName', 'N/A')
                cve_tags = cve_item.get('cveTags', [])
                descriptions = cve_item.get('descriptions', [])
                references = cve_item.get('references', [])
                metrics = cve_item.get('metrics', {})
                weaknesses = cve_item.get('weaknesses', [])
                configurations = cve_item.get('configurations', [])
                vendor_comments = cve_item.get('vendorComments', [])

                description = next((desc.get('value') for desc in descriptions if desc.get('lang') == 'en'), 'N/A')

                queue.put({
                    'CVE ID': cve_id,
                    'Source Identifier': source_identifier,
                    'Vulnerability Status': vuln_status,
                    'Published Date': published_date,
                    'Last Modified Date': last_modified_date,
                    'Evaluator Comment': evaluator_comment,
                    'Evaluator Solution': evaluator_solution,
                    'Evaluator Impact': evaluator_impact,
                    'CISA Exploit Add': cisa_exploit_add,
                    'CISA Action Due': cisa_action_due,
                    'CISA Required Action': cisa_required_action,
                    'CISA Vulnerability Name': cisa_vulnerability_name,
                    'CVE Tags': cve_tags,
                    'Description': description,
                    'References': ', '.join([ref.get('url', 'N/A') for ref in references]),
                    'Metrics': metrics,
                    'Weaknesses': weaknesses,
                    'Configurations': configurations,
                    'Vendor Comments': vendor_comments
                })

            total_results = data.get('totalResults', 0)
            if start_index + results_per_page >= total_results:
                break

            start_index += results_per_page
            await asyncio.sleep(6)  # Respect NVD API rate limits

    queue.put("DONE")


def save_data_to_csv(queue, output_file):
    data_items = []
    while True:
        item = queue.get()
        if item == "DONE":
            break
        data_items.append(item)
        if len(data_items) >= 100:  # Write in batches of 100
            df = pd.DataFrame(data_items)
            df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
            data_items = []
            print(f"Batch of 100 items saved to {output_file}")

    if data_items:
        df = pd.DataFrame(data_items)
        df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
        print(f"Remaining items saved to {output_file}")


async def main():
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / '../data/nvd_data'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'nvd_cve_data.csv'
    queue = Queue()
    writer_process = Process(target=save_data_to_csv, args=(queue, output_file))
    writer_process.start()

    last_modified = read_last_modified_date()
    current_time = datetime.now(timezone.utc).isoformat() + 'Z'

    params = {}
    if last_modified:
        params['lastModStartDate'] = last_modified
        params['lastModEndDate'] = current_time

    await extract_data(queue, BASE_URL_CVE, params)
    queue.put("DONE")
    writer_process.join()

    # Update the last modified date
    if os.path.exists(output_file):
        df = pd.read_csv(output_file)
        if not df.empty:
            last_modified_date = df['Last Modified Date'].max()
            write_last_modified_date(last_modified_date)


if __name__ == "__main__":
    asyncio.run(main())
