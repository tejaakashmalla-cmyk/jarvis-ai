import re
from pathlib import Path


class ErrorParser:
    """
    Parses runtime errors from different languages.

    Currently supports:
        - Python
    Future:
        - Node.js
        - React
        - FastAPI
        - Flutter
    """

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def parse(self, stderr: str):

        if not stderr:

            return {
                "success": True
            }

        parser = self._parse_python(stderr)

        if parser:

            return parser

        return {
            "success": False,
            "raw": stderr
        }

    # -------------------------------------------------
    # Python Parser
    # -------------------------------------------------

    def _parse_python(self, stderr):

        pattern = (
            r'File "(.+?)", line (\d+).*?\n'
            r'([A-Za-z_][A-Za-z0-9_]*): (.+)$'
        )

        match = re.search(
            pattern,
            stderr,
            re.MULTILINE | re.DOTALL
        )

        if not match:
            return None

        file_path = match.group(1)

        return {

            "success": False,

            "language": "python",

            "file": self._relative(file_path),

            "line": int(match.group(2)),

            "error_type": match.group(3),

            "message": match.group(4).strip()

        }

    # -------------------------------------------------
    # Relative Path
    # -------------------------------------------------

    def _relative(self, file_path):

        path = Path(file_path)

        parts = list(path.parts)

        if "projects" in parts:

            idx = parts.index("projects")

            return str(

                Path(

                    *parts[idx + 2:]

                )

            )

        return str(path)

    # -------------------------------------------------
    # Pretty Print
    # -------------------------------------------------

    def summary(self, error):

        print("\n========== RUNTIME ERROR ==========\n")

        for key, value in error.items():

            print(f"{key:12}: {value}")

        print("\n===================================\n")