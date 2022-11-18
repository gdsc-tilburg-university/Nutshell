from queue import Queue
from frontend.main import renderGUI
from recording.service import RecordingService
from speech_to_text.service import WhisperService
from summarization.service import SummaryService
import threading

if __name__ == "__main__":
    renderGUI()

    audioSegmentQueue = Queue()
    audioSegmentQueue.join()

    transcribedTextQueue = Queue()
    transcribedTextQueue.join()

    recordingService = RecordingService(audioSegmentQueue)
    whisperService = WhisperService(audioSegmentQueue, transcribedTextQueue)
    summaryService = SummaryService(transcribedTextQueue, useApi=False)

    recordingService.start()
    whisperService.start()
    summaryService.start()
