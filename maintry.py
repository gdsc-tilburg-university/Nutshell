import sounddevice as sd
from os import getcwd
from scipy.io.wavfile import write

duration = 10
sample_rate = 44100

duration = 30  # seconds
recording = sd.rec(frames = duration * sample_rate, samplerate= sample_rate, channels=1)
print("Started recording")

sd.wait()
print("finished recording")

filename = f"{getcwd()}\\audio.wav"

write(filename=filename, rate=sample_rate, data=recording)



