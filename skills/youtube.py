class YouTubeSkill:

    def __init__(self, browser):

        self.browser = browser

    def execute(self, query):

        command = f"open youtube and play {query}"

        return self.browser.execute(command)