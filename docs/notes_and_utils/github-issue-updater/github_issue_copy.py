import json

import requests

# Set up your personal access token and repository details
GITHUB_TOKEN = "<insert PAT token>"
OLD_REPO_OWNER = "gshiva"
OLD_REPO_NAME = "pygptcourse"
NEW_REPO_OWNER = "bpbpublications"
NEW_REPO_NAME = "Modern-Python-Programming-using-ChatGPT"

# Headers for the requests
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_milestones(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/milestones"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for request errors
    return response.json()


def create_milestone(repo_owner, repo_name, milestone):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/milestones"
    data = {
        "title": milestone["title"],
        "state": milestone["state"],
        "description": milestone.get("description", ""),
        "due_on": milestone.get("due_on"),
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Check for request errors
    return response.json()


def get_issues(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?state=all"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for request errors
    return response.json()


def create_issue(repo_owner, repo_name, issue, milestone_map):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    data = {
        "title": issue["title"],
        "body": issue["body"],
        "assignees": [a["login"] for a in issue.get("assignees", [])],
        "labels": [label["name"] for label in issue.get("labels", [])],
        "milestone": milestone_map.get(issue.get("milestone", {}).get("title")),
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Check for request errors
    return response.json()


def main():
    # Step 1: Get milestones from the old repository
    old_milestones = get_milestones(OLD_REPO_OWNER, OLD_REPO_NAME)
    milestone_map = {}

    # Step 2: Create milestones in the new repository and map them
    for milestone in old_milestones:
        new_milestone = create_milestone(NEW_REPO_OWNER, NEW_REPO_NAME, milestone)
        milestone_map[milestone["title"]] = new_milestone["number"]

    # Step 3: Get issues from the old repository
    old_issues = get_issues(OLD_REPO_OWNER, OLD_REPO_NAME)

    # Step 4: Create issues in the new repository, linking to milestones
    for issue in old_issues:
        create_issue(NEW_REPO_OWNER, NEW_REPO_NAME, issue, milestone_map)

    print("Milestones and issues have been successfully transferred.")


if __name__ == "__main__":
    main()
