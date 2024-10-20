import time
import serial
from serial_manager import SERIAL_SETTINGS



class TerminalData:
	def __init__(self):
		self.data = ""

	def write_char(self, char):
		self.data += char

	def clear(self):
		self.data = ""


terminal_data = TerminalData()


class Reponse:
	def __init__(self, sucessful = False, data = None):
		self._successful = sucessful
		self._data = data
	
	def successful(self):
		return self._successful
	
	def data(self):
		return self._data


def wait_for(target: str = None, exclude: list = [], timeout=20.0):
	start_time = time.time()
	found = False

	while time.time() - start_time < timeout:
		if target and target in terminal_data.data:
			if all(ex not in terminal_data.data for ex in exclude):
				found = True
				break
		time.sleep(0.1)

	data = terminal_data.data
	terminal_data.clear()
	return Reponse(found, data)


def send(data: str):
	# port = SERIAL_SETTINGS["port"]
	# baudrate = SERIAL_SETTINGS["baudrate"]
	# ser = serial.Serial(
	# 	port=port,
	# 	baudrate=baudrate,
	# 	parity=serial.PARITY_NONE,
	# 	stopbits=serial.STOPBITS_ONE,
	# 	bytesize=serial.EIGHTBITS
	# )
	# ser.write(data)
	print(data)