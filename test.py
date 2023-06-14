# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import json
import os

import requests

TOKEN = os.environ["STASH_HTTP_ACCESS_TOKEN"]
BASE_URL = "stash.doclerholding.com"
PROJECT_KEY = "MSYS"
REPOSITORY_SLUG = "manager"
PR_ID = "85"

URL = f"http://{BASE_URL}/rest/api/latest/projects/{PROJECT_KEY}/repos/{REPOSITORY_SLUG}/pull-requests/{PR_ID}/diff"

if TOKEN is None:
    raise Exception("Please set the environment variable 'STASH_HTTP_ACCESS_TOKEN'")

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

response = requests.get(URL, headers=HEADERS)

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
print(response.json())

