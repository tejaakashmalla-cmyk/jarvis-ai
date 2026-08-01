from pathlib import Path

from coding.specs.project_spec import ProjectSpec


class CodePlanner:
    """
    Plans the order in which files should be generated.

    The goal is to ensure dependencies are generated before
    the files that import or use them.
    """

    # --------------------------------------------------
    # Create Generation Order
    # --------------------------------------------------

    def create_plan(self, spec: ProjectSpec):

        files = list(spec.files)

        priority = []

        # ------------------------------------------
        # Configuration Files
        # ------------------------------------------

        priority.extend(

            self._collect(

                files,

                [
                    ".gitignore",
                    "README.md",
                    "requirements.txt",
                    "package.json",
                    ".env.example"
                ]

            )

        )

        # ------------------------------------------
        # Models
        # ------------------------------------------

        priority.extend(

            self._contains(

                files,

                [

                    "model",

                    "models"

                ]

            )

        )

        # ------------------------------------------
        # Database / Storage
        # ------------------------------------------

        priority.extend(

            self._contains(

                files,

                [

                    "database",

                    "db",

                    "storage",

                    "repository"

                ]

            )

        )

        # ------------------------------------------
        # Services
        # ------------------------------------------

        priority.extend(

            self._contains(

                files,

                [

                    "service",

                    "services"

                ]

            )

        )

        # ------------------------------------------
        # Utilities
        # ------------------------------------------

        priority.extend(

            self._contains(

                files,

                [

                    "util",

                    "utils",

                    "helper"

                ]

            )

        )

        # ------------------------------------------
        # Controllers
        # ------------------------------------------

        priority.extend(

            self._contains(

                files,

                [

                    "controller",

                    "controllers"

                ]

            )

        )

        # ------------------------------------------
        # Views / Pages
        # ------------------------------------------

        priority.extend(

            self._contains(

                files,

                [

                    "view",

                    "views",

                    "page",

                    "pages"

                ]

            )

        )

        # ------------------------------------------
        # Entry Point LAST
        # ------------------------------------------

        entry = spec.entry_point.replace("\\", "/")

        remaining = []

        for file in files:

            path = file.path.replace("\\", "/")

            if path == entry:

                continue

            remaining.append(file)

        priority.extend(remaining)

        for file in files:

            if file.path.replace("\\", "/") == entry:

                priority.append(file)

        # ------------------------------------------
        # Remove Duplicates
        # ------------------------------------------

        ordered = []

        seen = set()

        for file in priority:

            path = file.path.replace("\\", "/")

            if path not in seen:

                ordered.append(file)

                seen.add(path)

        return ordered

    # --------------------------------------------------
    # Collect Exact Files
    # --------------------------------------------------

    def _collect(self, files, names):

        result = []

        remaining = []

        names = {

            n.lower()

            for n in names

        }

        for file in files:

            filename = Path(file.path).name.lower()

            if filename in names:

                result.append(file)

            else:

                remaining.append(file)

        files[:] = remaining

        return result

    # --------------------------------------------------
    # Collect Contains
    # --------------------------------------------------

    def _contains(self, files, keywords):

        result = []

        remaining = []

        for file in files:

            path = file.path.lower()

            found = False

            for keyword in keywords:

                if keyword in path:

                    found = True
                    break

            if found:

                result.append(file)

            else:

                remaining.append(file)

        files[:] = remaining

        return result

    # --------------------------------------------------
    # Pretty Print
    # --------------------------------------------------

    def summary(self, ordered):

        print("\n========== GENERATION ORDER ==========\n")

        for i, file in enumerate(ordered, start=1):

            print(f"{i:02d}. {file.path}")

        print("\n======================================\n")