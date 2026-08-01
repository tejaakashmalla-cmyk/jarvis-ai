import json
from pathlib import Path


class TemplateLoader:

    def __init__(self):

        self.template_dir = Path(__file__).parent / "templates"

    # --------------------------------------------------
    # Load Template
    # --------------------------------------------------

    def load(self, language):

        path = self.template_dir / f"{language.lower()}.json"

        if not path.exists():

            raise FileNotFoundError(
                f"Template '{language}' not found."
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    # --------------------------------------------------
    # Get Files
    # --------------------------------------------------

    def get_files(self, language):

        template = self.load(language)

        return template.get("files", [])

    # --------------------------------------------------
    # Get Folders
    # --------------------------------------------------

    def get_folders(self, language):

        template = self.load(language)

        return template.get("folders", [])

    # --------------------------------------------------
    # Install Command
    # --------------------------------------------------

    def get_install_command(self, language):

        template = self.load(language)

        return template.get("install", "")

    # --------------------------------------------------
    # Run Command
    # --------------------------------------------------

    def get_run_command(self, language):

        template = self.load(language)

        return template.get("run", "")

    # --------------------------------------------------
    # Available Templates
    # --------------------------------------------------

    def available_templates(self):

        return sorted(

            file.stem

            for file in self.template_dir.glob("*.json")

        )