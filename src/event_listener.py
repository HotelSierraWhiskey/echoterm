from typing import List
from PySide6.QtCore import Signal, QObject
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


class WorkerSignals(QObject):
	output_ready = Signal(str)
	error_occurred = Signal(str)


def wait_for(target: str = None, exclude: list = [], on_event=None, timeout=5.0):
	start_time = time.time()
	found_event = Event()

	def runner():
		while time.time() - start_time < timeout:
			# Check if the target is in the terminal data and not in the exclude list
			if target and target in terminal_data.data:
				if all(ex not in terminal_data.data for ex in exclude):
					if on_event:
						on_event(target)
					found_event.set()
					break
			time.sleep(0.1)
		if not found_event.is_set():
			if on_event:
				on_event(None)

	Thread(target=runner).start()
	return found_event


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
