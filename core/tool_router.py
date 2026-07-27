import subprocess
import os
import webbrowser


class ToolRouter:

    def execute(self, command):

        command = command.lower()

        try:

            # -----------------
            # Websites
            # -----------------

            if "youtube" in command:
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube."

            elif "google" in command:
                webbrowser.open("https://www.google.com")
                return "Opening Google."

            elif "gmail" in command:
                webbrowser.open("https://mail.google.com")
                return "Opening Gmail."

            elif "github" in command:
                webbrowser.open("https://github.com")
                return "Opening GitHub."

            elif "chatgpt" in command:
                webbrowser.open("https://chat.openai.com")
                return "Opening ChatGPT."

            # -----------------
            # Desktop Apps
            # -----------------

            elif "calculator" in command or "calc" in command:
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