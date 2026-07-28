from pathlib import Path


class FileEditor:

    def create_file(self, path, content=""):

        path = Path(path)

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding="utf-8")

        return str(path)

    def read_file(self, path):

        return Path(path).read_text(encoding="utf-8")

    def overwrite(self, path, content):

        Path(path).write_text(content, encoding="utf-8")