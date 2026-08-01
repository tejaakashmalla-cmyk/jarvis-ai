from pathlib import Path


class FileEditor:

    def __init__(self):
        pass

    # ------------------------------------------
    # Write File
    # ------------------------------------------

    def write_file(self, path, content):

        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return file_path

    # ------------------------------------------
    # Read File
    # ------------------------------------------

    def read_file(self, path):

        file_path = Path(path)

        if not file_path.exists():
            return ""

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    # ------------------------------------------
    # Append File
    # ------------------------------------------

    def append_file(self, path, content):

        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            file_path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return file_path

    # ------------------------------------------
    # Replace Entire File
    # ------------------------------------------

    def replace_file(self, path, content):

        return self.write_file(
            path,
            content
        )

    # ------------------------------------------
    # File Exists
    # ------------------------------------------

    def exists(self, path):

        return Path(path).exists()

    # ------------------------------------------
    # Delete File
    # ------------------------------------------

    def delete_file(self, path):

        file_path = Path(path)

        if file_path.exists():

            file_path.unlink()

            return True

        return False