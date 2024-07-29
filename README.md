# Overview

The script conmon.py is designed to parse and process vulnerability data from an Excel file, generating a comprehensive report in a new Excel file. It handles various data categorizations such as plugin counts, vulnerability severities, and device types, and it provides visualizations through charts.

### Dependencies
1. Python 3.12  
2. pandas: `For data manipulation and analysis.`
3. xlsxwriter: `For creating Excel files.`
4. datetime: `For handling date and time data.`
5. argparse: `For parsing command-line options and arguments.`
6. re: `For regular expression matching operations.` 

### Main Features
1. Excel File Parsing: `Reads an Excel file containing vulnerability data.`
2. Data Filtering: `Ignores specified plugin IDs during data processing.`
3. Worksheet Generation: `Dynamically creates worksheets for different data categories.`
4. Data Insertion: `Populates worksheets with processed data.`
5. Chart Generation: `Creates pie charts to visualize vulnerabilities by severity.`
6. Report Generation: `Outputs a final report in Excel format with comprehensive data and charts.`

### Functions
1. generate_worksheets(): `Initializes worksheets for the Excel report.`
2. add_report_data(report_data_list, the_file): `Inserts detailed vulnerability data into the 'Full Report' worksheet.`
3. add_vuln_info(vuln_list, the_file): `Categorizes vulnerabilities by severity and updates respective worksheets.`
4. add_cvss_info(cvss_data, the_file): `Processes and inserts CVSS-related data.`
5. add_device_type(device_info, the_file): `Inserts device type information based on host data.`
6. add_ms_process_info(proc_info, the_file): `Adds information about running processes from Microsoft systems.`
7. add_plugin_info(plugin_count): `Updates the worksheet with plugin count information.`
8. begin_parsing(): `Orchestrates the parsing and processing of the Excel file based on specified arguments.`

### Example Usage

Notice: No file extension specified

```Bash
python main.py -l nessus_files -o reports/combined_report
```

To run the script, use the following command:

```Bash
python main.py -f input_file.xlsx -o output_file
```

Optional arguments include:  
`-f or --file`: Input Excel file containing vulnerability data.  
`-o or --output`: Output Excel file for the final report.  
`-l or --list_files`: Directory containing multiple Excel files to process.  
`-d or --debug`: Enable debug mode for detailed logging.  
`-v or --verbose`: Enable verbose mode for additional information.  
`-h or --help`: Display help message and exit.  
`-s or --severity`: Severity level to filter vulnerabilities.  
`-t or --type`: Device type to filter vulnerabilities.  
`-p or --process`: Process name to filter vulnerabilities.  
`-c or --cvss`: CVSS score to filter vulnerabilities.  
`-m or --ms_process`: Microsoft process name to filter vulnerabilities.   
`-pl or --plugin`: Plugin ID to filter vulnerabilities.    
`-pf or --plugin_file`: File containing plugin IDs to filter vulnerabilities.  
`-i or --ignore_id`: Comma-separated plugin IDs to ignore.  
`-ig or --ignore_id_file`: File containing plugin IDs to ignore.  

### Error Handling

The script includes error handling for file reading issues and ensures that only valid data is processed. Errors are logged to the console with appropriate messages.

## Data sources

Tenable data sources:

https://www.tenable.com/plugins  

| Type                                    | URL                                                                                                                                            |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| newset\_plugins                         | [https://www.tenable.com/plugins/feeds?sort=newest](https://www.tenable.com/plugins/feeds?sort=newest) |
| updated\_plugins                        | [https://www.tenable.com/plugins/feeds?sort=updated](https://www.tenable.com/plugins/feeds?sort=updated) |
| newest\_nessus\_plugins                 | [https://www.tenable.com/plugins/feeds?sort=updated\&type=nessus](https://www.tenable.com/plugins/feeds?sort=updated&type=nessus) |
| updated\_nessus\_plugins                | [https://www.tenable.com/plugins/feeds?sort=updated\&type=nessus](https://www.tenable.com/plugins/feeds?sort=updated&type=nessus) |
| newest\_web\_app\_scanning\_plugins     | [https://www.tenable.com/plugins/feeds?sort=newest\&type=was](https://www.tenable.com/plugins/feeds?sort=newest&type=was) |
| updated\_web\_app\_scanning\_plugins    | [https://www.tenable.com/plugins/feeds?sort=updated\&type=was](https://www.tenable.com/plugins/feeds?sort=updated&type=was) |
| newest\_nessus\_network\_monitor\_plugins | [https://www.tenable.com/plugins/feeds?sort=newest\&type=nnm](https://www.tenable.com/plugins/feeds?sort=newest&type=nnm) |
| updated\_nessus\_network\_monitor\_plugins | [https://www.tenable.com/plugins/feeds?sort=updated\&type=nnm](https://www.tenable.com/plugins/feeds?sort=updated&type=nnm) |
| newest\_log\_correlation\_engine\_plugins | [https://www.tenable.com/plugins/feeds?sort=newest\&type=lce](https://www.tenable.com/plugins/feeds?sort=newest&type=lce) |
| updated\_log\_correlation\_engine\_plugins | [https://www.tenable.com/plugins/feeds?sort=updated\&type=lce](https://www.tenable.com/plugins/feeds?sort=updated&type=lce) |

FunctionName URL
newset_plugins https://www.tenable.com/plugins/feeds?sort=newest
updated_plugins https://www.tenable.com/plugins/feeds?sort=updated
newest_nessus_plugins https://www.tenable.com/plugins/feeds?sort=updated&type=nessus
updated_nessus_plugins https://www.tenable.com/plugins/feeds?sort=updated&type=nessus
newest_web_app_scanning_plugins https://www.tenable.com/plugins/feeds?sort=newest&type=was
updated_web_app_scanning_plugins https://www.tenable.com/plugins/feeds?sort=updated&type=was
newest_nessus_network_monitor_plugins https://www.tenable.com/plugins/feeds?sort=newest&type=nnm
updated_nessus_network_monitor_plugins https://www.tenable.com/plugins/feeds?sort=updated&type=nnm
newest_log_correlation_engine_plugins https://www.tenable.com/plugins/feeds?sort=newest&type=lce
updated_log_correlation_engine_plugins https://www.tenable.com/plugins/feeds?sort=updated&type=lce

NVD data sources

| Type                                    | Description                                                                                                                                            |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| CVE and CPE APIs                        | An alternative to the traditional vulnerability data feed files. The APIs are far more flexible and offer a richer dataset in a single interface compared to the JSON Vulnerability Feeds and CPE Match Feed. |
| JSON Vulnerability Feeds                | Each vulnerability in the file includes a description and associated reference links from the CVE® dictionary feed, as well as CVSS base metrics, vulnerable product configuration, and weakness categorization. |
| CPE Match Feed                          | A feed that provides the product/platform applicability statement to CPE URI matching based on the CPEs in the official CPE dictionary.                 |
| Vulnerability Translation Feeds         | Translations of vulnerability feeds.                                                                                                                   |
| Vulnerability Vendor Comments           | Comments provided by vendors regarding a particular flaw affecting within a product.                                                                   |
| CPE Dictionary                          | Dictionary containing a list of products.                                                                                                              |
| Common Configuration Enumeration (CCE) Reference Data | Reference data for common configuration items.                                                                                                         |figuration Enumeration (CCE) Reference Data	Reference data for common configuration items.



The nessusparser.py script processes Nessus XML files to generate a comprehensive Excel report. Here's a detailed breakdown of the sequence of events, data sources, and target columns/worksheet mappings:
Sequence of Events:
1. Argument Parsing: The script starts by parsing command-line arguments to get the directory containing Nessus files and the output file name.
2. File Handling: It checks for Nessus files in the specified directory and handles scenarios where no files are found or there are too many files.
3. Worksheet Initialization: Initializes various worksheets in an Excel workbook for different types of data.
Parsing Nessus Files: Each Nessus file is parsed to extract vulnerability data, device information, and other relevant details.
5. Data Insertion: Extracted data is inserted into the appropriate worksheets.
6. Graph Generation: Generates graphs based on the severity of vulnerabilities.
7. Finalizing Report: Saves the Excel workbook with all the data and graphs.
Data Source from XML:
Host Attributes: Includes IP, FQDN, and NetBIOS name.
Vulnerability Details: Plugin ID, name, output, severity, CVSS scores, etc.
Device Information: Type and confidence level from specific plugins.
Process Information: Details about running processes from specific plugins.
Target Columns and Worksheets:
Overview: Summary of the report.
Graphs: Visual representations of data.
Full Report: Detailed vulnerability data including IP, port, severity, plugin details, CVSS scores, etc.
CVSS Overview: Aggregated CVSS score information.
Device Type: Information about detected devices.
Severity Worksheets (Critical, High, Medium, Low, Informational): Data categorized by severity.
MS Running Process Info: Information about Microsoft processes.
Plugin Counts: Counts of occurrences of each plugin.
Example of Data Mapping to Worksheets:
For the "Full Report" worksheet:

Columns:
- IP Address
- Port
- FQDN
- Vulnerability Publication Date
- Severity
- Risk Factor
- Plugin ID
- Plugin Name
- Description
- CVE Information
- CVSS Scores

Each piece of data extracted from the XML files is mapped to these columns in the Excel report, providing a detailed and structured overview of the vulnerabilities identified by the Nessus scans. The script uses lxml.etree for parsing XML and xlsxwriter for creating and managing the Excel report.