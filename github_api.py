import requests
import time
import os
from models import Repository

# GitHub GraphQL API endpoint and authentication token
GITHUB_API_URL = "https://api.github.com/graphql"
TOKEN = os.getenv("GITHUB_TOKEN")

def run_query(query):
    # Send a POST request to the GitHub GraphQL API with the provided query
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Raise an error if the request fails
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    
def parse_repositories(edges):
    """Convert raw GraphQL repo data into immutable Repository objects."""
    repos = []
    for edge in edges:
        node = edge["node"]
        # Map API response fields to internal Repository model
        repos.append(
            Repository(
                repo_id=node["databaseId"],
                name=node["name"],
                owner=node["owner"]["login"],
                stars=node["stargazerCount"],
            )
        )
    return repos

def check_rate_limit():
    # Query the API's current rate limit status
    query = """
    {
      rateLimit {
        limit
        cost
        remaining
        resetAt
      }
    }
    """
    data = run_query(query)
    info = data["data"]["rateLimit"]
    remaining = info["remaining"]
    reset_at = info["resetAt"]

    # Pause execution if approaching the rate limit threshold
    if remaining < 100:
        print(f"Rate limit almost reached. Waiting until reset at {reset_at}...")
        wait_time = 60  # could compute actual reset time difference
        time.sleep(wait_time)