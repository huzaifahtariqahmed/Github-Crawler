import psycopg2
from models import Repository

def get_connection():
    # Establish a new PostgreSQL database connection
    return psycopg2.connect(
        host="localhost",
        database="github_data",
        user="user",
        password="1234"
    )

def create_table():
    """Ensure the repositories table exists."""
    conn = get_connection()
    cur = conn.cursor()
    # Create the repositories table if it doesn't already exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id SERIAL PRIMARY KEY,
            repo_id BIGINT UNIQUE,
            name TEXT NOT NULL,
            owner TEXT NOT NULL,
            stars INT,
            last_updated TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table ready.")

def insert_repositories(repos: list[Repository]):
    """Insert or update repositories immutably."""
    if not repos:
        return
    conn = get_connection()
    cur = conn.cursor()
    # Insert each repository, updating stars if it already exists
    for r in repos:
        cur.execute("""
            INSERT INTO repositories (repo_id, name, owner, stars)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_id) DO UPDATE SET
                stars = EXCLUDED.stars,
                last_updated = NOW();
        """, (r.repo_id, r.name, r.owner, r.stars))
    conn.commit()
    cur.close()
    conn.close()