from dataclasses import dataclass

@dataclass(frozen=True)
class Repository:
    repo_id: int
    name: str
    owner: str
    stars: int