from playwright.sync_api import sync_playwright


class BrowserAutomation:

    # -----------------------------
    # YouTube Automation
    # -----------------------------

    def open_youtube(self, query):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(
                "https://www.youtube.com",
                wait_until="networkidle"
            )

            # Accept cookies if shown
            try:
                page.get_by_role("button", name="Accept all").click(timeout=3000)
            except:
                pass

            # Search
            page.locator("input[name='search_query']").wait_for(timeout=10000)

            search = page.locator("input[name='search_query']")

            search.click()

            search.fill(query)

            search.press("Enter")

            # Wait for results
            page.wait_for_selector("ytd-video-renderer", timeout=10000)

            # Play first video
            page.locator("ytd-video-renderer").first.click()

            print(f"Playing '{query}' on YouTube...")

            # Keep browser open
            page.wait_for_timeout(1000000)

    # -----------------------------
    # Google Automation
    # -----------------------------

    def search_google(self, query):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(
                "https://www.google.com",
                wait_until="networkidle"
            )

            # Accept cookies if shown
            try:
                page.get_by_role("button", name="Accept all").click(timeout=3000)
            except:
                pass

            # Search box
            search = page.locator("textarea[name='q']")

            search.wait_for(timeout=10000)

            search.fill(query)

            search.press("Enter")

            print(f"Searching Google for '{query}'...")

            # Keep browser open
            page.wait_for_timeout(1000000)

    # -----------------------------
    # Open GitHub
    # -----------------------------

    def open_github(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(
                "https://github.com",
                wait_until="networkidle"
            )

            page.wait_for_timeout(1000000)

    # -----------------------------
    # Open ChatGPT
    # -----------------------------

    def open_chatgpt(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(
                "https://chatgpt.com",
                wait_until="networkidle"
            )

            page.wait_for_timeout(1000000)