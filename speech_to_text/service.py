from queue import Queue
import threading
import whisper
from os import getcwd
import time

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
            segment.export(filename, format="wav")

            start = time.time()
            result = self.model.transcribe(filename)['text']
            print(
                f"took {round(time.time() - start, 1)} seconds to process {len(segment)}ms of audio")

            with lock:
                transcribedTextStore.append(result)

            print(f" Transcription: {result}")
            self.transcribedTextQueue.put(result)
            self.audioSegmentQueue.task_done()
