from skills.registry import SkillRegistry

from skills.youtube import YouTubeSkill
from skills.google import GoogleSkill
from skills.desktop import DesktopSkill

from agents.browser_agent import BrowserAgent
from core.tool_router import ToolRouter


def build_registry():

    registry = SkillRegistry()

    browser = BrowserAgent()

    desktop = ToolRouter()

    registry.register(
        "browser.youtube.play",
        YouTubeSkill(browser)
    )

    registry.register(
        "browser.google.search",
        GoogleSkill(browser)
    )

    registry.register(
        "desktop.open",
        DesktopSkill(desktop)
    )

    return registry