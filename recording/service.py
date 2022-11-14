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

        self.sample_rate: int = 44100
        self.minimum_segment_length: int = 20
        self.maximum_segment_length: int = 30

        self.audioSegmentQueue = audioSegmentQueue
        self.audioBuffer = None
        self.input = sounddevice.InputStream(
            samplerate=self.sample_rate, channels=1, blocksize=self.maximum_segment_length*self.sample_rate, callback=self.process_new_audio_block)

    def process_new_audio_block(self, indata: numpy.ndarray, frames, time, status) -> None:
        if self.audioBuffer is None:
            self.audioBuffer = indata
        else:
            self.audioBuffer = numpy.concatenate((self.audioBuffer, indata))

        while (cutoff := self.get_silent_slice_position()):
            self.audioSegmentQueue.put(self.audioBuffer[:cutoff])
            self.audioBuffer = self.audioBuffer[cutoff:]
            print(
                f"Cutting segment of {cutoff//self.sample_rate}s Audiobuffer: {len(self.audioBuffer)} ({len(self.audioBuffer)//self.sample_rate}s) Segment queue: {self.audioSegmentQueue.qsize()}")

    def get_silent_slice_position(self):
        segment = AudioSegment(
            self.audioBuffer.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=self.audioBuffer.dtype.itemsize,
            channels=1
        )

        silences = detect_silence(
            segment, min_silence_len=200, silence_thresh=-6)

        # look for a silent cutoff point
        for start, stop in silences:
            if stop >= self.maximum_segment_length*1000 and start > self.minimum_segment_length*1000:
                return int(start * self.sample_rate / 1000)

        # if no silence found and segment length too long
        if len(segment) >= self.maximum_segment_length*1000:
            return 30 * self.sample_rate

        return None

    def run(self):
        global isRecording

        # "with" activates the recording stream
        with self.input:
            while isRecording:
                print("recording: ", True)
                sleep(100)
            else:
                print("recording: ", False)


if __name__ == "__main__":
    audioSegmentQueue = Queue()
    audioSegmentQueue.join()

    recordingService = RecordingService(audioSegmentQueue)
    recordingService.start()
