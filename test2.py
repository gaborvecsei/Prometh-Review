import argparse
import os
import subprocess

import openai
import requests

TOKEN = os.environ["STASH_HTTP_ACCESS_TOKEN"]
if not TOKEN:
    raise ValueError("STASH_HTTP_ACCESS_TOKEN is not set")


def get_args():
    parser = argparse.ArgumentParser(description="AI Pull Request reviewer")
    parser.add_argument("--base-url", default="stash.doclerholding.com", type=str)
    parser.add_argument("-p", "--project-key", default="MSYS", type=str, help="Project key")
    parser.add_argument(
        "-c",
        "--nb-context-lines",
        default=10,
        type=int,
        help="how much lines to include before and after a changed line? Reduce it if you have problems with the script."
    )
    parser.add_argument("-r", "--repo", required=True, type=str, help="Slug of the repo")
    parser.add_argument("-id", "--pull-request-id", required=True, type=int, help="ID for the pull request")
    parser.add_argument("-d", "--show-diff-only", action="store_true", help="Show diff only, no AI checks")
    parser.add_argument("-i",
                        "--interactive",
                        action="store_true",
                        help="You can continue to chat about the PR with the AI")
    args = parser.parse_args()
    return args


BASE_URL = args.base_url
PROJECT_KEY = args.project_key
REPOSITORY_SLUG = args.repo
PR_ID = args.pull_request_id

headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

url_diff = f"http://{BASE_URL}/rest/api/latest/projects/{PROJECT_KEY}/repos/{REPOSITORY_SLUG}/pull-requests/{PR_ID}/diff"
response = requests.get(url_diff, headers=headers)
pr_diff_data = response.json()

url_info = f"http://{BASE_URL}/rest/api/latest/projects/{PROJECT_KEY}/repos/{REPOSITORY_SLUG}/pull-requests/{PR_ID}"
response = requests.get(url_info, headers=headers)
pr_info_data = response.json()

nb_change_context_lines = args.nb_context_lines
# Last commit of the PR
commit_new = pr_diff_data["toHash"]
# This is from where the branch was created
commit_old = pr_diff_data["fromHash"]
# PR description
# TODO: we need to fetch this automatically
description = f"""Title: {pr_info_data['title']}
Description: {pr_info_data['description']}"""

print("Info")
print(f"Commit hashes:\nFrom: {commit_old}\nTo: {commit_new}")
print(description)
print(f"PR link: {pr_info_data['links']['self'][0]['href']}")

# TODO: we should discard binaries, jupyter ntoebooks and other things like these
diff_output = subprocess.check_output(["git", "diff", f"-U{nb_change_context_lines}", commit_old, commit_new])
diff_output = diff_output.decode("utf-8")

if args.show_diff_only:
    print(diff_output)
    exit(0)

prompt = f"""Your task is:
    - Review the code changes and provide feedback - concentrate only on the changes!
    - Separately point out the bugs, security issues, missed best-practices and your feedback
    - If there are any bugs, highlight them (and use 'BUG' tag at the start of the line).
    - Provide details on missed use of best-practices.
    - Does the code do what it says in the commit messages?
    - Do not highlight minor issues and nitpicks.
    - Use bullet points if you have multiple comments.
    - Provide security recommendations if there are any.
    - Be concise and to the point.

    You are provided with the code changes (diffs) in a unidiff format.
    Do not provide feedback yet. I will follow-up with a description of the change in a new message.

"""

pr_description_message = f"""A description was given to help you assist in understand why these changes were made.
The description was provided in a markdown format. Do not provide feedback yet.
I will follow-up with the code changes in diff format in a new message.

{description}
"""

diff_message = f"""Diff in unidiff format:

{diff_output}
"""

final_message = """All code changes have been provided.
Please provide me with your code review based on all the changes, context & title provided
"""

messages = [{
    "role": "system",
    "content": prompt
}, {
    "role": "user",
    "content": pr_description_message
}, {
    "role": "user",
    "content": diff_message
}, {
    "role": "user",
    "content": final_message
}]

# TODO: truncate input if necessary

chat_completion: dict = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
response = chat_completion["choices"][0]["message"]["content"]
usage_metrics = chat_completion["usage"]

print(usage_metrics)
print(response)
