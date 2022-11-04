import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from os import getcwd


def record(duration: int = 10):
    fs = 44100
    myrecording = sd.rec(duration * fs, samplerate=fs,
                         channels=2, dtype='float64')
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete , Play Audio")
    target = f'{getcwd()}\\audio\\latest.wav'
    write(target, rate=44100, data=myrecording)
    return target


def audio_transcription(audiofile: str) -> str:
    model = whisper.load_model("base")
    result = model.transcribe(audiofile)
    return result["text"]


transcription = audio_transcription(record())
print(transcription)
