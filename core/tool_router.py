import subprocess
import os


class ToolRouter:

    def execute(self, command):

        command = command.lower()

        try:

            if "calculator" in command or "calc" in command:
                subprocess.Popen("calc.exe")
                return "Opening Calculator."

            elif "notepad" in command:
                subprocess.Popen("notepad.exe")
                return "Opening Notepad."

            elif "paint" in command:
                subprocess.Popen("mspaint.exe")
                return "Opening Paint."

            elif "explorer" in command or "file explorer" in command:
                subprocess.Popen("explorer.exe")
                return "Opening File Explorer."

            elif "chrome" in command:
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                ]

                for path in chrome_paths:
                    if os.path.exists(path):
                        subprocess.Popen(path)
                        return "Opening Chrome."

                return "Chrome is not installed."

            elif "vscode" in command or "visual studio code" in command:

                subprocess.Popen("code")
                return "Opening VS Code."

            return None

        except Exception as e:

            return f"Tool Error: {e}"