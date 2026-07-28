class SkillRegistry:

    def __init__(self):

        self.skills = {}

    def register(self, name, skill):

        self.skills[name] = skill

    def execute(self, name, **kwargs):

        skill = self.skills.get(name)

        if skill is None:
            return None

        return skill.execute(**kwargs)