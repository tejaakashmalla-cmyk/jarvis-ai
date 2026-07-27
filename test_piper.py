import subprocess
from playsound3 import playsound

text = "Hello Akash. I am Jarvis. Nice to finally speak with you."

subprocess.run(
    [
        "piper/piper.exe",
        "--model",
        "voice/voices/en_US-lessac-medium.onnx",
        "--output_file",
        "voice/output.wav",
    ],
    input=text.encode("utf-8"),
)

print("Voice generated successfully!")

playsound("voice/output.wav")