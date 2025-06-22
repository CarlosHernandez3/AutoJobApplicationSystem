from playwright.sync_api import sync_playwright
import os
import time

COOKIE_PATH = "linkedin_cookies.json"
SAVED_JOBS_URL = "https://www.linkedin.com/my-items/saved-jobs/"

def save_new_session(context):
    context.storage_state(path=COOKIE_PATH)
    print("New session saved.")

def is_logged_out(page):
    # Check for login form or redirected login URL
    return "login" in page.url.lower() or page.query_selector("input#username") is not None

def ensure_logged_in(context):
    page = context.new_page()
    page.goto(SAVED_JOBS_URL)
    time.sleep(3)

    if is_logged_out(page):
        print("Session expired or not logged in.")
        page.goto("https://www.linkedin.com/login")
        input("Please log in manually, then press ENTER to continue...")
        save_new_session(context)
    else:
        print("Successfully logged in with saved session.")

    return page

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Use existing session if it exists, else create new
        if os.path.exists(COOKIE_PATH):
            context = browser.new_context(storage_state=COOKIE_PATH)
        else:
            context = browser.new_context()

        page = ensure_logged_in(context)

        # You’re now logged in | start scraping
        page.goto(SAVED_JOBS_URL)
        time.sleep(5)

        print("Ready to scrape saved jobs...")

        browser.close()

if __name__ == "__main__":
    main()
