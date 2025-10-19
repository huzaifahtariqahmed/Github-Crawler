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

if __name__ == "__main__":
    create_table()
