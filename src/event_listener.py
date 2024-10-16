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
    found_event = Event()  # Event to signal when the target is found

    def runner():
        while time.time() - start_time < timeout:
            # Check if the target is in the terminal data and not in the exclude list
            if target and target in terminal_data.data:
                if all(ex not in terminal_data.data for ex in exclude):
                    # If the target is found and exclusions are not present
                    print("found")

                    # If there's an event callback, invoke it
                    if on_event:
                        on_event(target)

                    found_event.set()  # Signal that the target was found
                    break

            # Sleep for a short period to avoid busy waiting (polling interval)
            time.sleep(0.1)

        # If the loop finishes and the timeout is reached
        if not found_event.is_set():  # Check if the target wasn't found
            print(f"Timeout reached. '{target}' not found.")

    t = Thread(target=runner)
    t.start()

    # Wait for the result or timeout
    found_event.wait(timeout)  # This will block until the target is found or timeout occurs

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
