CREATE TABLE IF NOT EXISTS repositories (
    id SERIAL PRIMARY KEY,
    repo_id BIGINT UNIQUE,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    stars INT,
    last_updated TIMESTAMP DEFAULT NOW()
);
