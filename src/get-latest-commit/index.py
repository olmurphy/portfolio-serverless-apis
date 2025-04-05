import json
import requests
import os

def lambda_handler(event, context=None):
    """
    Retrieves the latest commit from a specified branch of a GitHub repository.

    Args:
        event (dict): AWS Lambda event input, containing repository owner, name, and branch.
        - GET /repos/{owner}/{repo}/commits/latest?branch={branch}
        context (obj): AWS Lambda context object.

    Returns:
        dict: A dictionary containing the latest commit's SHA and timestamp, or an error message.
    """

    try:
        # Retrieve repository owner, name, and branch from event or environment variables
        owner = event.get('owner') or os.environ.get('GITHUB_OWNER')
        repo = event.get('repo') or os.environ.get('GITHUB_REPO')
        branch = event.get('branch') or os.environ.get('GITHUB_BRANCH') or "main" #Default branch is Main.
        github_token = os.environ.get('GITHUB_TOKEN') # Optional token for increased rate limits.

        if not owner or not repo:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Repository owner and name are required."}),
            }

        # Construct the GitHub API URL
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}&per_page=1"

        headers = {
            "Accept": "application/vnd.github+json",
            'X-GitHub-Api-Version': '2022-11-28',
        }

        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"

        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        commits = response.json()

        if commits:
            latest_commit = commits[0]
            commit_sha = latest_commit["sha"]
            commit_timestamp = latest_commit["commit"]["author"]["date"]

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "commit_sha": commit_sha,
                    "commit_timestamp": commit_timestamp
                }),
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "No commits found on the specified branch."}),
            }

    except requests.exceptions.HTTPError as e:
        return {
            "statusCode": e.response.status_code,
            "body": json.dumps({"message": f"GitHub API error: {e}"}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"An error occurred: {e}"}),
        }