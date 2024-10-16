from typing import List
import time
from threading import Thread, Event


class TerminalData:
    def __init__(self):
        self.data = ""

    def write_char(self, char):
        self.data += char

    def clear(self):
        self.data = ""


terminal_data = TerminalData()


def wait_for(target: str = None, exclude: List[str] = [], on_event=None, timeout=5.0):
    start_time = time.time()
    found_event = Event()

    def runner():
        while time.time() - start_time < timeout:
            if target and target in terminal_data.data:
                if all(ex not in terminal_data.data for ex in exclude):
            
                    print("found")
                    if on_event:
                        on_event(target)
                    found_event.set()
                    break

            time.sleep(0.1)

        if not found_event.is_set():
            print(f"Timeout reached. '{target}' not found.")

    t = Thread(target=runner)
    t.start()

    found_event.wait(timeout)

    return found_event.is_set()

class EventListener:
    def __init__(self, target: str = None, exclude: List[str] = [], on_event=None, timeout=5.0):
        self.target = target
        self.exclude = exclude
        self.on_event = on_event
        self.timeout = timeout
        self.source = ""

    def read_char(self, c):
        self.source += c
        if self.target in self.source and self.exclude not in self.source:
            print(f"Found: {self.target}")
            self.source = ""

    def beep(self):
        print("BEEP!")
