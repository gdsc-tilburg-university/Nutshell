from scipy.io.wavfile import write
from queue import Queue
import threading
import whisper
from os import getcwd

transcribedTextStore = []
lock = threading.Lock()


class WhisperService(threading.Thread):
    def __init__(self, audioSegmentQueue: Queue, transcribedTextQueue: Queue):
        threading.Thread.__init__(self)
        self.audioSegmentQueue = audioSegmentQueue
        self.transcribedTextQueue = transcribedTextQueue
        self.model = whisper.load_model("small.en")

    def run(self):
        global transcribedTextStore
        
        while True:
            segment = self.audioSegmentQueue.get()

            filename = f'{getcwd()}\\audio\\latest.wav'
            write(filename, rate=44100, data=segment)

            padded_audio = whisper.pad_or_trim(whisper.load_audio(filename))
            result = self.model.transcribe(padded_audio)['text']

            with lock:
                transcribedTextStore.append(result)

            print(f" Transcription: {result}")
            self.transcribedTextQueue.put(result)
            self.audioSegmentQueue.task_done()
