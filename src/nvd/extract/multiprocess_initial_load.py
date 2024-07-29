import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import pandas as pd
import ssl
from datetime import datetime, timezone
from multiprocessing import Process, Queue
from pathlib2 import Path

# Load environment variables
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

async def fetch_data(session, url, params):
    headers = {
        'apiKey': NVD_API_KEY
    }

    async with session.get(url, headers=headers, params=params, ssl=ssl_context) as response:
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Response status code: {response.status}")
        json_response = await response.json()
        return json_response

async def extract_data(queue):
    start_index = 0
    results_per_page = 2000

    async with aiohttp.ClientSession() as session:
        while True:
            params = {
                'startIndex': start_index,
                'resultsPerPage': results_per_page
            }

            print(f"Fetching CVE data starting at index {start_index}")
            data = await fetch_data(session, BASE_URL_CVE, params)
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

                cvss_v3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})

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
                    'CVSSv3 Version': cvss_v3.get('version', 'N/A'),
                    'CVSSv3 Vector String': cvss_v3.get('vectorString', 'N/A'),
                    'CVSSv3 Attack Vector': cvss_v3.get('attackVector', 'N/A'),
                    'CVSSv3 Attack Complexity': cvss_v3.get('attackComplexity', 'N/A'),
                    'CVSSv3 Privileges Required': cvss_v3.get('privilegesRequired', 'N/A'),
                    'CVSSv3 User Interaction': cvss_v3.get('userInteraction', 'N/A'),
                    'CVSSv3 Scope': cvss_v3.get('scope', 'N/A'),
                    'CVSSv3 Confidentiality Impact': cvss_v3.get('confidentialityImpact', 'N/A'),
                    'CVSSv3 Integrity Impact': cvss_v3.get('integrityImpact', 'N/A'),
                    'CVSSv3 Availability Impact': cvss_v3.get('availabilityImpact', 'N/A'),
                    'CVSSv3 Base Score': cvss_v3.get('baseScore', 'N/A'),
                    'CVSSv3 Base Severity': cvss_v3.get('baseSeverity', 'N/A'),
                    'CVSSv3 Exploit Code Maturity': metrics.get('exploitCodeMaturity', 'N/A'),
                    'CVSSv3 Remediation Level': metrics.get('remediationLevel', 'N/A'),
                    'CVSSv3 Report Confidence': metrics.get('reportConfidence', 'N/A'),
                    'CVSSv3 Temporal Score': metrics.get('temporalScore', 'N/A'),
                    'CVSSv3 Temporal Severity': metrics.get('temporalSeverity', 'N/A'),
                    'CVSSv3 Confidentiality Requirement': metrics.get('confidentialityRequirement', 'N/A'),
                    'CVSSv3 Integrity Requirement': metrics.get('integrityRequirement', 'N/A'),
                    'CVSSv3 Availability Requirement': metrics.get('availabilityRequirement', 'N/A'),
                    'CVSSv3 Modified Attack Vector': metrics.get('modifiedAttackVector', 'N/A'),
                    'CVSSv3 Modified Attack Complexity': metrics.get('modifiedAttackComplexity', 'N/A'),
                    'CVSSv3 Modified Privileges Required': metrics.get('modifiedPrivilegesRequired', 'N/A'),
                    'CVSSv3 Modified User Interaction': metrics.get('modifiedUserInteraction', 'N/A'),
                    'CVSSv3 Modified Scope': metrics.get('modifiedScope', 'N/A'),
                    'CVSSv3 Modified Confidentiality Impact': metrics.get('modifiedConfidentialityImpact', 'N/A'),
                    'CVSSv3 Modified Integrity Impact': metrics.get('modifiedIntegrityImpact', 'N/A'),
                    'CVSSv3 Modified Availability Impact': metrics.get('modifiedAvailabilityImpact', 'N/A'),
                    'CVSSv3 Environmental Score': metrics.get('environmentalScore', 'N/A'),
                    'CVSSv3 Environmental Severity': metrics.get('environmentalSeverity', 'N/A')
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
    output_dir = base_dir / 'data/nvd_data'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'nvd_data.csv'
    queue = Queue()
    writer_process = Process(target=save_data_to_csv, args=(queue, output_file))
    writer_process.start()

    await extract_data(queue)
    queue.put("DONE")
    writer_process.join()

if __name__ == "__main__":
    asyncio.run(main())