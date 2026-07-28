class GoogleSkill:

    def __init__(self, browser):

        self.browser = browser

    def execute(self, query):

        command = f"search google {query}"

        return self.browser.execute(command)