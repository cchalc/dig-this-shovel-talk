"""
GitHub Projects Sync Module

Uses GitHub GraphQL API to sync Fizzy card states to GitHub Projects v2.
"""

import requests
from typing import Optional


class GitHubProjectSync:
    """Sync Fizzy card states to GitHub Projects v2."""

    GRAPHQL_URL = "https://api.github.com/graphql"
    REST_URL = "https://api.github.com"

    def __init__(self, token: str, owner: str, project_number: int, repo: str = "dig-this-shovel-talk"):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.project_number = project_number
        self._project_id: Optional[str] = None
        self._status_field_id: Optional[str] = None
        self._status_options: dict = {}

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _graphql(self, query: str, variables: dict = None) -> dict:
        """Execute GraphQL query."""
        response = requests.post(
            self.GRAPHQL_URL,
            headers=self._headers(),
            json={"query": query, "variables": variables or {}}
        )
        response.raise_for_status()
        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
        return result["data"]

    def _get_project_metadata(self) -> None:
        """Fetch project ID, status field ID, and status options."""
        if self._project_id:
            return

        query = """
        query($owner: String!, $number: Int!) {
          user(login: $owner) {
            projectV2(number: $number) {
              id
              fields(first: 20) {
                nodes {
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    options {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """

        data = self._graphql(query, {"owner": self.owner, "number": self.project_number})
        project = data["user"]["projectV2"]
        self._project_id = project["id"]

        # Find Status field
        for field in project["fields"]["nodes"]:
            if field and field.get("name") == "Status":
                self._status_field_id = field["id"]
                self._status_options = {
                    opt["name"]: opt["id"]
                    for opt in field.get("options", [])
                }
                break

    def _get_project_item_id(self, issue_number: int) -> Optional[str]:
        """Get the project item ID for an issue."""
        self._get_project_metadata()

        query = """
        query($owner: String!, $repo: String!, $number: Int!) {
          repository(owner: $owner, name: $repo) {
            issue(number: $number) {
              projectItems(first: 10) {
                nodes {
                  id
                  project {
                    id
                  }
                }
              }
            }
          }
        }
        """

        data = self._graphql(query, {
            "owner": self.owner,
            "repo": self.repo,
            "number": issue_number
        })

        items = data["repository"]["issue"]["projectItems"]["nodes"]
        for item in items:
            if item["project"]["id"] == self._project_id:
                return item["id"]

        return None

    def update_issue_status(self, issue_number: int, status: str) -> dict:
        """Update the status of an issue in the project."""
        self._get_project_metadata()

        item_id = self._get_project_item_id(issue_number)
        if not item_id:
            return {"success": False, "error": "Issue not found in project"}

        option_id = self._status_options.get(status)
        if not option_id:
            return {
                "success": False,
                "error": f"Status '{status}' not found. Available: {list(self._status_options.keys())}"
            }

        mutation = """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $projectId
            itemId: $itemId
            fieldId: $fieldId
            value: { singleSelectOptionId: $optionId }
          }) {
            projectV2Item {
              id
            }
          }
        }
        """

        self._graphql(mutation, {
            "projectId": self._project_id,
            "itemId": item_id,
            "fieldId": self._status_field_id,
            "optionId": option_id
        })

        return {"success": True, "status": status}

    def close_issue(self, issue_number: int) -> dict:
        """Close a GitHub issue."""
        url = f"{self.REST_URL}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        response = requests.patch(
            url,
            headers=self._headers(),
            json={"state": "closed"}
        )
        response.raise_for_status()
        return {"success": True, "state": "closed"}

    def add_comment(self, issue_number: int, body: str) -> dict:
        """Add a comment to a GitHub issue."""
        url = f"{self.REST_URL}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        response = requests.post(
            url,
            headers=self._headers(),
            json={"body": body}
        )
        response.raise_for_status()
        return {"success": True, "comment_id": response.json()["id"]}

    def add_label(self, issue_number: int, label: str) -> dict:
        """Add a label to a GitHub issue."""
        url = f"{self.REST_URL}/repos/{self.owner}/{self.repo}/issues/{issue_number}/labels"
        response = requests.post(
            url,
            headers=self._headers(),
            json={"labels": [label]}
        )
        response.raise_for_status()
        return {"success": True, "label": label}
