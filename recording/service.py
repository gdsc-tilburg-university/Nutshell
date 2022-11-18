from queue import Queue
import threading
from pydub import AudioSegment
import speech_recognition as sr
import io

isRecording = threading.Event()


class RecordingService(threading.Thread):
    def __init__(self, audioSegmentQueue: Queue):
        threading.Thread.__init__(self)
        self.r = sr.Recognizer()
        self.r.energy_threshold = 500
        self.r.pause_threshold = 0.8
        self.r.dynamic_energy_threshold = False
        self.sample_rate: int = 16000
        self.audioSegmentQueue = audioSegmentQueue

    def run(self):
        global isRecording
        isRecording.set()

        with sr.Microphone(sample_rate=self.sample_rate) as source:
            while True:
                print("waiting...")
                isRecording.wait()
                print("recording...")

                # minimum segment length 20s
                # whisper expects 30s fragments, so shorter fragments are processed relatively slowly
                # while len(segment) < 20000:
                #     limit = (30000 - len(segment)) / 1000
                #     audio = self.r.listen(source, phrase_time_limit=limit)
                #     data = io.BytesIO(audio.get_wav_data())

                #     if not segment:
                #         segment = AudioSegment.from_file(data)
                #     else:
                #         segment = segment.append(AudioSegment.from_file(data))

                #     print(f"current segment length {len(segment)}")

                audio = self.r.listen(source, phrase_time_limit=30)
                data = io.BytesIO(audio.get_wav_data())
                segment = AudioSegment.from_file(data)
                print(f"current segment length {len(segment)}")

                # add segment to the queue
                self.audioSegmentQueue.put(segment)


if __name__ == "__main__":
    audioSegmentQueue = Queue()
    audioSegmentQueue.join()

    recordingService = RecordingService(audioSegmentQueue)
    recordingService.start()
