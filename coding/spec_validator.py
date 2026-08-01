from pathlib import Path

from coding.specs.project_spec import (
    ProjectSpec,
    FolderSpec,
    FileSpec,
    ClassSpec,
    DependencySpec
)


class SpecValidator:

    """
    Validates and repairs a ProjectSpec before code generation.
    """

    def validate(self, spec: ProjectSpec) -> ProjectSpec:

        self._remove_duplicate_folders(spec)
        self._remove_duplicate_files(spec)
        self._remove_duplicate_classes(spec)
        self._remove_duplicate_dependencies(spec)

        self._ensure_entry_point_exists(spec)
        self._ensure_class_files_exist(spec)
        self._ensure_parent_folders_exist(spec)

        return spec

    # --------------------------------------------------
    # Remove Duplicate Folders
    # --------------------------------------------------

    def _remove_duplicate_folders(self, spec):

        seen = set()
        folders = []

        for folder in spec.folders:

            path = folder.path.replace("\\", "/")

            if path not in seen:

                seen.add(path)

                folders.append(
                    FolderSpec(path)
                )

        spec.folders = folders

    # --------------------------------------------------
    # Remove Duplicate Files
    # --------------------------------------------------

    def _remove_duplicate_files(self, spec):

        seen = set()
        files = []

        for file in spec.files:

            path = file.path.replace("\\", "/")

            if path not in seen:

                seen.add(path)

                files.append(
                    FileSpec(
                        path,
                        file.purpose
                    )
                )

        spec.files = files

    # --------------------------------------------------
    # Remove Duplicate Classes
    # --------------------------------------------------

    def _remove_duplicate_classes(self, spec):

        seen = set()
        classes = []

        for cls in spec.classes:

            key = (
                cls.name,
                cls.file
            )

            if key not in seen:

                seen.add(key)

                classes.append(

                    ClassSpec(

                        cls.name,

                        cls.file,

                        cls.purpose

                    )

                )

        spec.classes = classes

    # --------------------------------------------------
    # Remove Duplicate Dependencies
    # --------------------------------------------------

    def _remove_duplicate_dependencies(self, spec):

        seen = set()

        deps = []

        for dep in spec.dependencies:

            name = dep.name.lower()

            if name not in seen:

                seen.add(name)

                deps.append(

                    DependencySpec(

                        dep.name,

                        dep.version

                    )

                )

        spec.dependencies = deps

    # --------------------------------------------------
    # Entry Point
    # --------------------------------------------------

    def _ensure_entry_point_exists(self, spec):

        if not spec.entry_point:

            if spec.language.lower() == "python":

                spec.entry_point = "src/main.py"

            elif spec.language.lower() == "react":

                spec.entry_point = "src/main.jsx"

            elif spec.language.lower() == "node":

                spec.entry_point = "src/index.js"

        exists = False

        for file in spec.files:

            if file.path == spec.entry_point:

                exists = True
                break

        if not exists:

            spec.files.append(

                FileSpec(

                    spec.entry_point,

                    "Application Entry Point"

                )

            )

    # --------------------------------------------------
    # Class Files
    # --------------------------------------------------

    def _ensure_class_files_exist(self, spec):

        existing = {

            file.path

            for file in spec.files

        }

        for cls in spec.classes:

            if cls.file not in existing:

                spec.files.append(

                    FileSpec(

                        cls.file,

                        f"Contains {cls.name}"

                    )

                )

                existing.add(cls.file)

    # --------------------------------------------------
    # Parent Folders
    # --------------------------------------------------

    def _ensure_parent_folders_exist(self, spec):

        folders = {

            folder.path

            for folder in spec.folders

        }

        for file in spec.files:

            parent = str(
                Path(file.path).parent
            ).replace("\\", "/")

            if parent == ".":

                continue

            if parent not in folders:

                spec.folders.append(

                    FolderSpec(parent)

                )

                folders.add(parent)

    # --------------------------------------------------
    # Pretty Print
    # --------------------------------------------------

    def summary(self, spec):

        print("\n========== PROJECT SPEC ==========\n")

        print("Folders")

        for folder in spec.folders:

            print(f"  📁 {folder.path}")

        print()

        print("Files")

        for file in spec.files:

            print(f"  📄 {file.path}")

        print()

        print("Classes")

        for cls in spec.classes:

            print(

                f"  🔹 {cls.name}"

                f" -> {cls.file}"

            )

        print()

        print("Dependencies")

        for dep in spec.dependencies:

            print(f"  📦 {dep.name}")

        print("\n==================================\n")