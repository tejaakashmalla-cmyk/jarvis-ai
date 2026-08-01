import subprocess
from pathlib import Path


class Terminal:

    def __init__(self):
        pass

    # ---------------------------------------
    # Run Command
    # ---------------------------------------

    def run(self, command, cwd=None):

        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    # ---------------------------------------
    # Run Background Process
    # ---------------------------------------

    def run_background(self, command, cwd=None):

        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True
        )

        return process

    # ---------------------------------------
    # Install Python Package
    # ---------------------------------------

    def pip_install(self, package, cwd=None):

        return self.run(
            f"pip install {package}",
            cwd
        )

    # ---------------------------------------
    # Install Node Package
    # ---------------------------------------

    def npm_install(self, cwd=None):

        return self.run(
            "npm install",
            cwd
        )

    # ---------------------------------------
    # Run Python File
    # ---------------------------------------

    def run_python(self, filename, cwd=None):

        return self.run(
            f'python "{filename}"',
            cwd
        )

    # ---------------------------------------
    # Run Node Project
    # ---------------------------------------

    def run_node(self, cwd=None):

        return self.run(
            "npm run dev",
            cwd
        )

    # ---------------------------------------
    # Git Init
    # ---------------------------------------

    def git_init(self, cwd=None):

        return self.run(
            "git init",
            cwd
        )

    # ---------------------------------------
    # Git Add
    # ---------------------------------------

    def git_add(self, cwd=None):

        return self.run(
            "git add .",
            cwd
        )

    # ---------------------------------------
    # Git Commit
    # ---------------------------------------

    def git_commit(self, message, cwd=None):

        return self.run(
            f'git commit -m "{message}"',
            cwd
        )