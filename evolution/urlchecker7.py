import requests
import csv
import json
from tqdm import tqdm

# Input and output file paths
input_file = 'input_urls.tsv'  # Path to your input tab-delimited file
output_file = 'output_results.tsv'  # Path where you want to save the results
config_file = 'config.json'  # Path to your config file with GitHub token

# GitHub GraphQL API endpoint
github_graphql_url = "https://api.github.com/graphql"

# Load the GitHub token from the config file
with open(config_file, 'r') as f:
    config = json.load(f)
    github_token = config['github_token']

# Authorization header with the token
headers = {"Authorization": f"Bearer {github_token}"}

# GraphQL query to fetch total commits and issues
graphql_query = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    object(expression: "HEAD") {
      ... on Commit {
        history {
          totalCount
        }
      }
    }
    issues(states: OPEN) {
      totalCount
    }
  }
}
"""

# Function to extract repository owner and name from URL
def get_repo_owner_and_name(url):
    parts = url.split("/")[-2:]
    return parts[0], parts[1]

# Function to get total commit counts and issue counts using GitHub GraphQL API
def get_repo_stats(owner, name):
    variables = {"owner": owner, "name": name}
    try:
        response = requests.post(github_graphql_url, json={'query': graphql_query, 'variables': variables}, headers=headers)
        data = response.json()
        if 'errors' in data:
            return 0, 0
        commits_count = data['data']['repository']['object']['history']['totalCount'] if data['data']['repository']['object'] is not None else 0
        issues_count = data['data']['repository']['issues']['totalCount'] if data['data']['repository']['issues'] is not None else 0
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
            final_url = response.url
            results[url] = {"status": f"Moved to {final_url}"}
            owner, name = get_repo_owner_and_name(final_url)
            commits_count, issues_count = get_repo_stats(owner, name)
            results[url]['commits'] = commits_count
            results[url]['issues'] = issues_count
        else:
            owner, name = get_repo_owner_and_name(url)
            commits_count, issues_count = get_repo_stats(owner, name)
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
