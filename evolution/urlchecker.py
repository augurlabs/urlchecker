import requests
from bs4 import BeautifulSoup

urls = [
    "https://github.com/samsung/flare_v8_build",
    "https://github.com/samsung/flare_llvm",
    "https://github.com/samsung/rome",
    "https://github.com/samsung/plug-ur-tool",
    "https://github.com/samsung/tedeu5"
]

results = {}

for url in urls:
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

for url, status in results.items():
    print(f"{url}: {status}")
