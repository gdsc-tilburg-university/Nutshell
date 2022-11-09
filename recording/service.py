from queue import Queue
import threading
import sounddevice
import numpy
from pydub import AudioSegment
from pydub.silence import detect_silence

audioSegmentQueue = []
lock = threading.Lock()


class RecordingService(threading.Thread):
    def __init__(self, audioSegmentQueue: Queue):
        threading.Thread.__init__(self)
        self.audioSegmentQueue = audioSegmentQueue
        self.audioBuffer = None
        self.maximum_segment_length: int = 10
        self.fs: int = 44100

    def stream_callback(self, indata: numpy.ndarray, frames, time, status) -> None:
        print("callback")
        if self.audioBuffer is None:
            self.audioBuffer = indata
        else:
            self.audioBuffer = numpy.concatenate((self.audioBuffer, indata))

        while cutoff := self.get_silent_cutoff_position():
            self.audioSegmentQueue.put(self.audioBuffer[:cutoff])
            self.segments.append(self.audioBuffer[:cutoff])
            self.audioBuffer = self.audioBuffer[:cutoff]
            print(
                f"Audiobuffer: {len(self.audioBuffer)} ({len(self.audioBuffer)//self.fs}s) Segment queue: {self.audioSegmentQueue.qsize()}")

    def get_silent_cutoff_position(self):
        channel1 = self.audioBuffer[:]

        segment = AudioSegment(
            channel1.tobytes(),
            frame_rate=self.fs,
            sample_width=channel1.dtype.itemsize,
            channels=1
        )

        silences = detect_silence(
            segment, min_silence_len=100, silence_thresh=-6)

        for i, startStop in enumerate(silences):
            if startStop[0] > self.maximum_segment_length*1000:
                return (None if silences[i-1] is None else silences[i-1][0]//1000 * self.fs)

    def run(self):
        input = sounddevice.InputStream(
            samplerate=self.fs, channels=1, blocksize=self.maximum_segment_length*self.fs, callback=self.stream_callback)
        with input:
            while True:
                pass


if __name__ == "__main__":
    audioSegmentQueue = Queue()
    audioSegmentQueue.join()

    recordingService = RecordingService(audioSegmentQueue)
    recordingService.start()
    recordingService.join()
