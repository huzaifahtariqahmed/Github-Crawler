import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="github_data",
        user="huzaifah",
        password="1234"
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
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
    print("Table created successfully!")
    
def insert_repositories(repos):
    if not repos:
        return  # no data to insert

    conn = get_connection()
    cur = conn.cursor()

    for r in repos:
        cur.execute("""
            INSERT INTO repositories (repo_id, name, owner, stars)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_id) DO UPDATE SET
                stars = EXCLUDED.stars,
                last_updated = NOW();
        """, (r['repo_id'], r['name'], r['owner'], r['stars']))

    conn.commit()
    cur.close()
    conn.close()