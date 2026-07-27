import subprocess
from playsound3 import playsound


class JarvisTTS:

    def __init__(self):

        self.model = "voice/voices/en_US-lessac-medium.onnx"

    def speak(self, text):

        subprocess.run(
            [
                "piper/piper.exe",
                "--model",
                self.model,
                "--output_file",
                "voice/output.wav",
                 "--length_scale",
                  "1.20"
            ],
            input=text.encode("utf-8"),
            check=True,
        )

        playsound("voice/output.wav")