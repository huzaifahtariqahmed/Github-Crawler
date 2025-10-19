from github_api import run_query, check_rate_limit
from db import insert_repositories, create_table

def fetch_repositories(target_count=1000):
    query_template = """
    {{
    search(query: "stars:>1", type: REPOSITORY, first: 100 {after_clause}) {{
        pageInfo {{
        endCursor
        hasNextPage
        }}
        edges {{
        node {{
            ... on Repository {{
            databaseId
            name
            owner {{ login }}
            stargazerCount
            }}
        }}
        }}
    }}
    }}
    """
    repos = []
    has_next_page = True
    cursor = None

    while has_next_page and len(repos) < target_count:
        after_clause = f', after: "{cursor}"' if cursor else ""
        query = query_template.format(after_clause=after_clause)
        result = run_query(query)
        edges = result["data"]["search"]["edges"]

        batch = []
        for edge in edges:
            node = edge["node"]
            batch.append({
                "repo_id": node["databaseId"],
                "name": node["name"],
                "owner": node["owner"]["login"],
                "stars": node["stargazerCount"]
            })

        insert_repositories(batch)  # save each batch in DB
        repos.extend(batch)
        print(f"Inserted {len(repos)} repos so far...")

        page_info = result["data"]["search"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        cursor = page_info["endCursor"]
        
        # Check rate limit after each batch
        check_rate_limit()

    print(f"Done! Total {len(repos)} repositories fetched and saved.")

if __name__ == "__main__":
    create_table()
    fetch_repositories(target_count=1000)
