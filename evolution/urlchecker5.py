import requests
import csv
import json
from tqdm import tqdm

# Input and output file paths
input_file = 'input_urls.tsv'  # Path to your input tab-delimited file
output_file = 'output_results.tsv'  # Path where you want to save the results
config_file = 'config.json'  # Path to your config file with GitHub token

# GitHub API base URL
github_api_url = "https://api.github.com/repos/"

# Load the GitHub token from the config file
with open(config_file, 'r') as f:
    config = json.load(f)
    github_token = config['github_token']

# Authorization header with the token
headers = {"Authorization": f"token {github_token}"}

# Function to extract repository name from URL
def get_repo_name(url):
    return "/".join(url.split("/")[-2:])

# Function to get commit counts and issue counts
def get_repo_stats(repo_name):
    commits_url = f"{github_api_url}{repo_name}/commits"
    issues_url = f"{github_api_url}{repo_name}/issues"
    
    try:
        commits_response = requests.get(commits_url, headers=headers)
        issues_response = requests.get(issues_url, headers=headers)
        
        commits_count = len(commits_response.json())
        issues_count = len(issues_response.json())
        
        return commits_count, issues_count
    except requests.exceptions.RequestException as e:
        return "Error", "Error"

# Dictionary to hold results
results = {}

# Read the URLs from the input file
with open(input_file, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='\t')
    urls = [row[0] for row in reader]

# Check each URL with a progress bar
for url in tqdm(urls, desc="Processing URLs", unit="url"):
    try:
        response = requests.get(url, allow_redirects=True, headers=headers)
        if response.status_code == 404:
            results[url] = {"status": "404 Not Found", "commits": None, "issues": None}
        elif response.history:  # Check if there was a redirect
            results[url] = {"status": f"Moved to {response.url}", "commits": None, "issues": None}
        else:
            repo_name = get_repo_name(url)
            commits_count, issues_count = get_repo_stats(repo_name)
            results[url] = {"status": "Active", "commits": commits_count, "issues": issues_count}
    except requests.exceptions.RequestException as e:
        results[url] = {"status": f"Error: {str(e)}", "commits": None, "issues": None}

# Write the results to the output file
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerow(['URL', 'Status', 'Commits', 'Issues'])  # Header
    for url, info in results.items():
        writer.writerow([url, info['status'], info['commits'], info['issues']])

print(f"Results have been saved to {output_file}")
