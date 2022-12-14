import sounddevice
from scipy.io.wavfile import write
from os import getcwd


def record(duration: int = 30, fs: int = 44100) -> str:
    recording = sounddevice.rec(duration * fs, samplerate=fs,
                                channels=1, dtype='float64')

    print("\nRecording Audio")
    sounddevice.wait()
    print("Audio recording complete, Transcribing")

    filename = f'{getcwd()}\\audio\\latest.wav'
    write(filename, rate=fs, data=recording)
    return filename
