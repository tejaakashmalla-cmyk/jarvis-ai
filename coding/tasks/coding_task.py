from dataclasses import dataclass


@dataclass
class CodingTask:

    project_name: str

    language: str

    framework: str = ""

    platform: str = ""

    ui: str = ""

    storage: str = ""

    architecture: str = ""

    testing: bool = False

    description: str = ""