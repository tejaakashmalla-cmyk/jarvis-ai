from pathlib import Path


class ProjectManager:

    def create_project(self, name: str):

        root = Path(name)

        root.mkdir(parents=True, exist_ok=True)

        return root

    def create_folder(self, root, folder):

        path = root / folder

        path.mkdir(parents=True, exist_ok=True)

        return path