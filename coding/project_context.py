from dataclasses import dataclass, field

from coding.specs.project_spec import ProjectSpec


@dataclass
class ProjectContext:
    """
    Live state of the project while Jarvis is building it.
    """

    spec: ProjectSpec

    generated_files: dict = field(default_factory=dict)
    generated_classes: dict = field(default_factory=dict)
    imports: dict = field(default_factory=dict)

    completed_steps: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    history: list = field(default_factory=list)

    current_file: str = ""
    remaining_files: list = field(default_factory=list)

    # --------------------------------------------------

    def add_file(self, path, content):

        self.generated_files[path] = content
        self.history.append(f"Generated {path}")

    # --------------------------------------------------

    def get_file(self, path):

        return self.generated_files.get(path)

    # --------------------------------------------------

    def add_class(self, class_name, file_path):

        self.generated_classes[class_name] = file_path

    # --------------------------------------------------

    def has_class(self, class_name):

        return class_name in self.generated_classes

    # --------------------------------------------------

    def add_import(self, file_path, import_name):

        self.imports.setdefault(file_path, []).append(import_name)

    # --------------------------------------------------

    def add_error(self, error):

        self.errors.append(error)

    # --------------------------------------------------

    def add_step(self, step):

        self.completed_steps.append(step)

    # --------------------------------------------------

    def set_current_file(self, file_path):

        self.current_file = file_path

    # --------------------------------------------------

    def set_remaining_files(self, files):

        self.remaining_files = files

    # --------------------------------------------------

    def summary(self):

        print("\n========== PROJECT CONTEXT ==========\n")

        print("Current File:")
        print(" ", self.current_file)
        print()

        print("Remaining Files:")
        for file in self.remaining_files:
            print(" ", file)
        print()

        print("Generated Files:")
        for file in self.generated_files:
            print(" ", file)
        print()

        print("Generated Classes:")
        for cls, file in self.generated_classes.items():
            print(f"  {cls} -> {file}")
        print()

        print("Errors:")
        for error in self.errors:
            print(" ", error)
        print()

        print("Completed Steps:")
        for step in self.completed_steps:
            print(" ", step)

        print("\n=====================================\n")