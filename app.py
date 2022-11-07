import threading
from frontend.main import ui


def startGuiService():
    thread = threading.Thread(target=ui.run)
    thread.start()

# def startTranscribingService():
#     thread = threading.Thread(target=)
#     thread.start()


if __name__ == "__main__":
    startGuiService()
