import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from playwright.async_api import async_playwright
import re
from utils.job_schema import JobPost
from utils.job_helpers import get_existing_job_urls, save_job_to_jsonl
from typing import List
import json

# Keywords to filter relevant jobs
KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "ml",
    "data engineer", "data engineering", "data science"
]

FAILED_JOBS_PATH = os.path.join("storage", "failed_jobs.jsonl")
os.makedirs(os.path.dirname(FAILED_JOBS_PATH), exist_ok=True)

def log_failed_job(raw_data, error_message):
    with open(FAILED_JOBS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"raw_data": raw_data, "error_message": error_message}) + "\n")

async def scrape_levels_fyi_jobs(url: str, existing_urls: set) -> List[JobPost]:
    jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        # Handle popup if it appears
        try:
            await page.wait_for_selector('button:has-text("Continue")', timeout=5000)
            await page.click('button:has-text("Continue")')
        except Exception:
            pass  # Popup did not appear, continue

        page_num = 1
        while True:
            print(f"Scraping page {page_num}...")
            try:
                await page.wait_for_selector('div[role="button"]', timeout=60000)
            except Exception:
                print(f"Warning: No job cards found after waiting on page {page_num}.")
                break
            job_cards = await page.query_selector_all('div[role="button"]')
            print(f"Found {len(job_cards)} job cards")
            for card in job_cards:
                try:
                    await card.click()
                    await page.wait_for_selector('div.job-details-header_jobTitleRow__ZU5Uc', timeout=5000)
                    title = await page.eval_on_selector('div.job-details-header_jobTitleRow__ZU5Uc', 'el => el.innerText')
                    details_row = await page.query_selector('p.job-details-header_detailsRow__4zP3I')
                    company = location = None
                    if details_row:
                        details_text = await details_row.inner_text()
                        parts = [part.strip() for part in details_text.split('•')]
                        if len(parts) >= 1:
                            company = parts[0]
                        if len(parts) >= 3:
                            location = parts[2]
                    try:
                        description = await page.eval_on_selector('section.job-details-about_aboutContainer__GxwKQ', 'el => el.innerText')
                    except Exception:
                        description = None
                    try:
                        apply_link = await page.eval_on_selector('div.job-details-header_externalLinkRow__fymrT a', 'el => el.href')
                    except Exception:
                        apply_link = None
                    if title and any(kw in title.lower() for kw in KEYWORDS):
                        tags = [kw for kw in KEYWORDS if kw in title.lower()]
                        job_url = apply_link or ""
                        if job_url and job_url not in existing_urls:
                            job = JobPost(
                                source="levels_fyi",
                                title=title.strip(),
                                company=company.strip() if company else None,
                                location=location.strip() if location else None,
                                url=job_url,
                                description=description.strip() if description else None,
                                tags=tags
                            )
                            jobs.append(job)
                            save_job_to_jsonl(job.model_dump())
                except Exception as e:
                    try:
                        card_html = await card.evaluate('el => el.outerHTML')
                    except Exception:
                        card_html = None
                    log_failed_job({"card_html": card_html}, str(e))
                    print(f"Failed to scrape a job card: {e}")
                    if card_html:
                        print(f"Card HTML: {card_html}\n---\n")
                    continue
            # Pagination: look for the next page button
            try:
                next_button = await page.query_selector('button:has(svg[data-testid="KeyboardArrowRightIcon"])')
                if next_button:
                    disabled = await next_button.get_attribute('disabled')
                    if disabled:
                        print("Next button is disabled. Stopping.")
                        break
                    await next_button.click()
                    await page.wait_for_timeout(4000)  # Wait for new jobs to load
                    page_num += 1
                else:
                    print("No next button found. Stopping.")
                    break
            except Exception as e:
                print(f"No more pages or failed to click next: {e}")
                break
        await browser.close()
    return jobs

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.levels.fyi/jobs/level/entry?postedAfterTimeType=days&postedAfterValue=7&jobId=92232280654652102"
    existing_urls = get_existing_job_urls()
    results = asyncio.run(scrape_levels_fyi_jobs(url, existing_urls))
    print(f"Appended {len(results)} new jobs to data/jobs.jsonl")
