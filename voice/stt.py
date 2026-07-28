from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile


class JarvisSTT:

    def __init__(self):

        print("Loading Whisper model...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("Whisper Ready!")

    def listen(self, seconds=5):

        samplerate = 16000

        print("Listening...")

        recording = sd.rec(
            int(seconds * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        write(
            temp.name,
            samplerate,
            recording
        )

        segments, info = self.model.transcribe(
            temp.name
        )

        text = ""

        for segment in segments:

            text += segment.text

        return text.strip()