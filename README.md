To set up the project environment:

```bash
# Create a new environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate GitCrawler

# Update the environment after modifying environment.yml
conda env update -f environment.yml --prune

# (Optional) Update requirements.txt from current environment
make update-reqs