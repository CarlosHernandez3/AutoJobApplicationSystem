import json
from typing import Set, Dict

def get_existing_job_urls(path="data/jobs.jsonl") -> Set[str]:
    urls = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                job = json.loads(line)
                if "url" in job:
                    urls.add(job["url"])
    except FileNotFoundError:
        pass  # File doesn't exist yet
    return urls

def save_job_to_jsonl(job: Dict, path="data/jobs.jsonl"):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(job) + "\n") 