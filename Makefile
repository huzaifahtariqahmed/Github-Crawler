# Makefile

ENV_NAME = GitCrawler

update-reqs:
	pip freeze > requirements.txt
