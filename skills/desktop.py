class DesktopSkill:

    def __init__(self, tools):

        self.tools = tools

    def execute(self, action):

        return self.tools.execute(action)