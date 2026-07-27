from automation.browser import BrowserAutomation


class BrowserAgent:

    def __init__(self):

        self.browser = BrowserAutomation()

    def execute(self, command):

        command = command.lower()

        # --------------------
        # YouTube
        # --------------------

        if "youtube" in command:

            query = ""

            if "play" in command:

                query = command.split("play", 1)[1].strip()

            if query == "":
                query = "Trending"

            self.browser.open_youtube(query)

            return f"Playing {query} on YouTube."

        # --------------------
        # Google
        # --------------------

        elif "google" in command:

            query = ""

            if "search" in command:

                query = command.split("search", 1)[1].strip()

            self.browser.search_google(query)

            return f"Searching Google for {query}."

        return None