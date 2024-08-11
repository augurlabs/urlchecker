# urlchecker
A simply python program that evaluates a return delimited list of URLs and determines if they are MOVED or REMOVED

Also, a separate URL Checker focused on GitHub, where additional metadata about live or moved URLs are captured. 
## Setup: 
1. Use the `config.json.example` file as a format for creating your own `config.json` file with your GitHub token inside it.
2. Create a python3 virtualenv. We used Python3.11 for testing, so something like `python3.11 -m venv /my/venv/directory`
3. Activate the virtualenv: `source /my/venv/directory/bin/activate`
4. Install required libraries: `pip install -r requirements.txt`
5. Put any URLs you wish to check into the `input_urls.tsv` file
6. Run the program. For GitHub, it would be `python github_url_checker7.py`
7. Wait and watch the progress
8. Check the results

## Included Data Files
1. input_urls_1.tsv - Set of repositories that failed collection during catch up in August, 2024
2. input_urls_2.tsv - Set of repositories in the process of collecting after being reset in August, 2024
3. input_urls_3.tsv - Set of repositories that failed collection a second time in August, 2024
4. input_urls_4.tsv - A more complete set of the same class of data as input_urls_3.tsv 

**output*<number>.tsv files correspond with the related input file number**
