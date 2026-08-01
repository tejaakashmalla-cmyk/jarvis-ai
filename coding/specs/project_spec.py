from dataclasses import dataclass, field


# --------------------------------------------------
# Class Specification
# --------------------------------------------------

@dataclass
class ClassSpec:

    name: str

    file: str

    purpose: str


# --------------------------------------------------
# File Specification
# --------------------------------------------------

@dataclass
class FileSpec:

    path: str

    purpose: str


# --------------------------------------------------
# Folder Specification
# --------------------------------------------------

@dataclass
class FolderSpec:

    path: str


# --------------------------------------------------
# Dependency Specification
# --------------------------------------------------

@dataclass
class DependencySpec:

    name: str

    version: str = ""


# --------------------------------------------------
# Project Specification
# --------------------------------------------------

@dataclass
class ProjectSpec:

    project_name: str

    language: str

    framework: str = ""

    entry_point: str = ""

    folders: list[FolderSpec] = field(default_factory=list)

    files: list[FileSpec] = field(default_factory=list)

    classes: list[ClassSpec] = field(default_factory=list)

    dependencies: list[DependencySpec] = field(default_factory=list)

    description: str = ""

    run_command: str = ""

    install_command: str = ""

    build_command: str = ""

    test_command: str = ""