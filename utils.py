import time
import threading

class Thread(threading.Thread):
    def __init__(self, target, callback):
        super().__init__()
        self.flag = threading.Event()
        self.target = target
        self.callback = callback

    def run(self):
        while not self.flag.is_set():
            is_done = self.target()
            if is_done:
                self.flag.set()
            time.sleep(1)
        self.callback()