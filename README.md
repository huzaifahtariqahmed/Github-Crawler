Perfect — you’ve structured your project beautifully, Huzaifah.
Now what you need is a **professional, detailed `README.md`** that:

* clearly explains what the project does,
* provides step-by-step setup instructions (both locally and via GitHub Actions), and
* demonstrates that you followed solid software engineering principles.

Here’s a complete, submission-ready version you can paste directly into your repo.

---

# 🚀 GitHub Crawler

A Python-based GitHub crawler that uses the **GitHub GraphQL API** to fetch repository data (name, owner, stars) for large-scale analytics.
The project stores results in **PostgreSQL**, supports **continuous daily crawling**, and is fully automated through a **GitHub Actions pipeline**.

---

## 📁 Project Structure

```
Github-Crawler/
│
├── .github/workflows/crawler.yml    # GitHub Actions workflow for automation
├── db.py                            # Database connection + table management logic
├── environment.yml                  # Conda environment definition
├── github_api.py                    # Handles GitHub GraphQL API queries
├── LICENSE
├── main.py                          # Orchestrator – runs the crawling and saving process
├── Makefile                         # Automates requirement exports
├── models.py                        # Immutable dataclass models (anti-corruption layer)
├── README.md
├── requirements.txt                 # Python dependencies (used by CI/CD)
├── schema.sql                       # Database schema used in GitHub Actions setup
└── test_db.py                       # Optional local DB connection test
```

---

## 🧠 Overview

This project fulfills Sofstica’s **AI Engineer Assignment** requirement to:

* Fetch star counts for 100,000 GitHub repositories using the **GraphQL API**.
* Store the results in a **PostgreSQL** database.
* Respect **API rate limits**.
* Automate the entire process using **GitHub Actions**.
* Follow **clean architecture** and **software engineering principles**.

---

## 🧱 Architecture & Design Principles

| Principle                  | Implementation                                                                         |
| -------------------------- | -------------------------------------------------------------------------------------- |
| **Separation of Concerns** | `github_api.py` handles data fetching; `db.py` handles storage; `main.py` coordinates. |
| **Anti-Corruption Layer**  | `models.py` defines internal dataclasses isolating app logic from GitHub API schemas.  |
| **Immutability**           | Repositories are represented as frozen dataclasses (no side effects).                  |
| **Scalability**            | Supports easy schema extension (issues, PRs, comments) and daily automated runs.       |
| **Automation**             | Full GitHub Actions pipeline with PostgreSQL service container.                        |

---

## 🧩 Key Components

### 1. `models.py`

Defines immutable data models to isolate the code from raw API data.

```python
@dataclass(frozen=True)
class Repository:
    repo_id: int
    name: str
    owner: str
    stars: int
```

### 2. `github_api.py`

Handles:

* GitHub GraphQL queries
* Pagination
* Rate limit checks
* Conversion to internal `Repository` objects

### 3. `db.py`

Manages:

* PostgreSQL connection
* Table creation
* Batched inserts with `ON CONFLICT` upsert logic for efficient updates

### 4. `main.py`

Coordinates the process:

1. Fetch repositories from GitHub
2. Insert into PostgreSQL
3. Respect rate limits during long crawls

---

## ⚙️ Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Github-Crawler.git
cd Github-Crawler
```

### 2. Set Up Environment

Using **conda**:

```bash
conda env create -f environment.yml
conda activate GitCrawler
```

To update the environment later:

```bash
conda env update -f environment.yml --prune
```

### 3. Run PostgreSQL Locally (Docker)

```bash
docker run --name github-postgres \
  -e POSTGRES_USER=huzaifah \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=github_data \
  -p 5432:5432 \
  -d postgres
```

### 4. Run Locally

Export your GitHub token for authentication:

```bash
export GITHUB_TOKEN=<your_personal_access_token>
python main.py
```

You’ll see progress as repositories are fetched and stored.

---

## 🧪 Testing Database Connection

To quickly verify DB connectivity:

```bash
python test_db.py
```

If it prints:

```
✅ Connection successful!
```

you’re ready to go.

---

## 🤖 GitHub Actions (Automated Run)

This project includes a workflow (`crawler.yml`) that:

1. Starts a Postgres service container
2. Runs schema setup
3. Executes the crawler
4. Dumps the database into a CSV file
5. Uploads it as an artifact

### How to Run It:

1. Push the repository to GitHub.
2. Navigate to the **Actions** tab.
3. Select **GitHub Crawler**.
4. Click **Run workflow** → select branch → **Run**.

When complete:

* You’ll see ✅ **Job succeeded**.
* Scroll down to **Artifacts** and download **`github-stars-data`** → contains `data.csv`.

---

## 🧠 Extensibility: Future Metadata (Issues, PRs, Comments)

To collect additional metadata:

* Add new dataclasses in `models.py` (e.g. `Issue`, `PullRequest`, `Comment`).
* Create corresponding tables in `schema.sql`.
* Extend `github_api.py` with GraphQL fragments for issues, PRs, etc.
* Use `ON CONFLICT` upserts to handle updates efficiently.

This modular structure allows adding new entity types **without modifying existing code**, only extending it.

---

## 🧹 Maintenance Commands

```bash
# Recreate environment
conda env create -f environment.yml

# Update dependencies
conda env update -f environment.yml --prune

# Export pip dependencies (used by CI)
make update-reqs
```

---

## 📜 License

This project is released under the [MIT License](LICENSE).