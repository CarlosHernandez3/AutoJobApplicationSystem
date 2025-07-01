import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from utils.job_schema import JobPost
from utils.job_helpers import get_existing_job_urls, save_job_to_jsonl
import json

SAVED_JOBS_URL = "https://github.com/vanshb03/New-Grad-2025?tab=readme-ov-file"

KEYWORDS = [
    "ml", "ai", "ml ops", "ml infra", "data engineer", "data science", "machine learning", "ai", "artificial intelligence",
    "data engineefailedr", "data engineering", "quantitative", "quant", "quantitative finance", "quantitative trading", "quantitative research", 
    "python", "algorithmic trader", "ml inference"
]

FAILED_JOBS_PATH = os.path.join("storage", "failed_jobs.jsonl")
os.makedirs(os.path.dirname(FAILED_JOBS_PATH), exist_ok=True)

def log_failed_job(raw_data, error_message, existing_urls):
    url = raw_data.get("url")
    if url and url in existing_urls:
        return  # Don't log if already saved
    with open(FAILED_JOBS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"raw_data": raw_data, "error_message": error_message}) + "\n")

def parse_job_li(li, existing_urls):
    a = li.find("a", href=True)
    if not a:
        return None
    title = a.get_text(strip=True)
    url = a["href"]
    if url.startswith("/"):
        url = f"https://github.com{url}"
    text = li.get_text(" ", strip=True)
    company = text.split("-", 1)[0].strip() if "-" in text else "Unknown"
    try:
        return JobPost(
            source="simplify_jobs_gh",
            title=title,
            company=company,
            url=url,
            tags=[]
        )
    except Exception as e:
        log_failed_job({"title": title, "company": company, "url": url, "li_text": text}, str(e), existing_urls)
        return None

def parse_job_row(row, existing_urls):
    cols = row.find_all("td")
    if len(cols) < 4:
        return None
    company = cols[0].get_text(strip=True)
    role = cols[1].get_text(strip=True)
    location = cols[2].get_text(" ", strip=True)
    a = cols[3].find("a", href=True)
    url = a["href"] if a else None
    if url and url.startswith("/"):
        url = f"https://github.com{url}"
    role_lower = role.lower()
    if not any(kw in role_lower for kw in KEYWORDS):
        return None
    try:
        return JobPost(
            source="simplify_jobs_gh",
            title=role,
            company=company,
            location=location,
            url=url or "",
            tags=[]
        )
    except Exception as e:
        log_failed_job({"company": company, "role": role, "location": location, "url": url}, str(e), existing_urls)
        return None

def is_relevant_job(job):
    title_lower = job.title.lower()
    return any(kw in title_lower for kw in KEYWORDS)

def main():
    existing_urls = get_existing_job_urls()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(SAVED_JOBS_URL)
        time.sleep(5)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        all_jobs = []
        for li in soup.find_all("li"):
            job = parse_job_li(li, existing_urls)
            if job and is_relevant_job(job):
                if job.url not in existing_urls:
                    all_jobs.append(job)
                    save_job_to_jsonl(job.model_dump())
        for table in soup.find_all("table"):
            rows = table.find_all("tr")[1:]
            for row in rows:
                job = parse_job_row(row, existing_urls)
                if job and job.url not in existing_urls:
                    all_jobs.append(job)
                    save_job_to_jsonl(job.model_dump())
        print(f"Extracted and saved {len(all_jobs)} new relevant jobs from the page.")
        browser.close()

if __name__ == "__main__":
    main()
