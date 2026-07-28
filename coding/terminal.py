import subprocess


class Terminal:

    def run(self, command, cwd=None):

        process = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True
        )

        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode
        }