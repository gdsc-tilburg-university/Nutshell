from scipy.io.wavfile import write
from queue import Queue
import threading
import whisper
import numpy as np
from recording.service import RecordingService
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

            # supposed to load numpy data directly into a useable format for whisper
            # does not seem to work (yet)

            # audio = np.frombuffer(segment, np.int16).astype(
            #     np.float32)*(1/32768.0)

            target = f'{getcwd()}\\audio\\latest.wav'
            write(target, rate=44100, data=segment)

            result = self.model.transcribe(
                whisper.pad_or_trim(whisper.load_audio(target)))['text']

            with lock:
                transcribedTextStore.append(result)

            print(f" Transcription: {result}")
            self.transcribedTextQueue.put(result)
            self.audioSegmentQueue.task_done()


if __name__ == "__main__":
    audioSegmentQueue = Queue()
    audioSegmentQueue.join()

    transcribedTextQueue = Queue()
    transcribedTextQueue.join()

    recordingService = RecordingService(audioSegmentQueue)
    whisperService = WhisperService(audioSegmentQueue, transcribedTextQueue)

    recordingService.start()
    whisperService.start()
