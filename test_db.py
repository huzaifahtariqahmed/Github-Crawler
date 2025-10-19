import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="github_data",
        user="huzaifah",
        password="1234"
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
