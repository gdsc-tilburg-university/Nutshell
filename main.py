import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from os import getcwd
import warnings


def record(duration: int = 10, fs: int = 44100) -> str:
    recording = sd.rec(duration * fs, samplerate=fs,
                       channels=1, dtype='float64')
    print("\nRecording Audio")
    sd.wait()
    print("Audio recording complete, Transcribing")
    target = f'{getcwd()}\\audio\\latest.wav'
    write(target, rate=fs, data=recording)
    return target


def audio_transcription(audiofile: str) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = whisper.load_model("small")
        result = model.transcribe(audiofile)
    print("Transcription complete\n")
    return result["text"]


transcription = audio_transcription(record())
print(transcription)
