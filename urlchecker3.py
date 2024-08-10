import requests
import csv
from tqdm import tqdm

# Input and output file paths
input_file = 'input_urls.tsv'  # Path to your input tab-delimited file
output_file = 'output_results.tsv'  # Path where you want to save the results

# Dictionary to hold results
results = {}

# Read the URLs from the input file
with open(input_file, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='\t')
    urls = [row[0] for row in reader]

# Check each URL with a progress bar
for url in tqdm(urls, desc="Processing URLs", unit="url"):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 404:
            results[url] = "404 Not Found"
        elif response.status_code in [301, 302]:
            results[url] = f"Moved to {response.url}"
        else:
            results[url] = "Active"
    except requests.exceptions.RequestException as e:
        results[url] = f"Error: {str(e)}"

# Write the results to the output file
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerow(['URL', 'Status'])  # Header
    for url, status in results.items():
        writer.writerow([url, status])

print(f"Results have been saved to {output_file}")
