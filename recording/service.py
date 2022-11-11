from queue import Queue
import threading
import sounddevice
import numpy
from pydub import AudioSegment
from pydub.silence import detect_silence
from time import sleep

isRecording = True


class RecordingService(threading.Thread):
    def __init__(self, audioSegmentQueue: Queue):
        threading.Thread.__init__(self)
        self.audioSegmentQueue = audioSegmentQueue
        self.audioBuffer = None
        self.minimum_segment_length: int = 20
        self.maximum_segment_length: int = 30
        self.fs: int = 44100
        self.input = sounddevice.InputStream(
            samplerate=self.fs, channels=1, blocksize=self.maximum_segment_length*self.fs, callback=self.stream_callback)

    def stream_callback(self, indata: numpy.ndarray, frames, time, status) -> None:
        if self.audioBuffer is None:
            self.audioBuffer = indata
        else:
            self.audioBuffer = numpy.concatenate((self.audioBuffer, indata))

        while (cutoff := self.get_silent_cutoff_position()):
            self.audioSegmentQueue.put(self.audioBuffer[:cutoff])
            self.audioBuffer = self.audioBuffer[cutoff:]
            print(
                f"Cutting segment of {cutoff//self.fs}s Audiobuffer: {len(self.audioBuffer)} ({len(self.audioBuffer)//self.fs}s) Segment queue: {self.audioSegmentQueue.qsize()}")

    def get_silent_cutoff_position(self):
        channel1 = self.audioBuffer[:]

        segment = AudioSegment(
            channel1.tobytes(),
            frame_rate=self.fs,
            sample_width=channel1.dtype.itemsize,
            channels=1
        )

        silences = detect_silence(
            segment, min_silence_len=200, silence_thresh=-6)

        for start, stop in silences:
            if stop >= self.maximum_segment_length*1000 and start > self.minimum_segment_length*1000:
                return int(start * self.fs / 1000)

        if len(segment) >= self.maximum_segment_length*1000:
            return int(len(segment) * self.fs / 1000)

        return None

    def run(self):
        global isRecording
        with self.input:
            while isRecording:
                print("recording: ", True)
                sleep(10)
            else:
                print("recording: ", False)


if __name__ == "__main__":
    audioSegmentQueue = Queue()
    audioSegmentQueue.join()

    recordingService = RecordingService(audioSegmentQueue)
    recordingService.start()
