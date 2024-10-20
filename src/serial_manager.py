from qtstrap import *
import serial


"""
Global serial settings

Global because scripts that runs in the application's code editor
use these settings as well.
"""
SERIAL_SETTINGS = {
	"port": None,
	"baudrate": None
}


class SerialConnection(QThread):
	"""
	The main serial interface.

	This runs a listener thread, forwarding received data to a `SerialManager`.
	Data transmission is handled by top level widgets via the `Serial` instance 
	member. Instances of `SerialConnection` are joined when communication sessions
	complete. Fresh instances are created when communication sessions are started.
	"""

	rx = Signal(str)

	def __init__(self, ser: serial.Serial, parent=None):
		super().__init__(parent=parent)
		self.ser = ser

	def run(self):
		"""
		Override of `QThread.run`. 
		Listens for bytes on the serial port.
		Decodes, and emits the data up to the `SerialManager`.
		"""
		while True:
			try:
				byte = self.ser.read()
				char = byte.decode()
				self.rx.emit(char)
			except Exception:
				break


class SerialManager(QWidget):
	"""
	The serial manager is responsible for starting and stopping
	the serial connection thread, and applying serial interface
	settings
	"""

	rx = Signal(str)

	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.conn = None

	def start_thread(self):
		"""
		Starts the listener thread for the serial port
		"""
		if not self.conn.isRunning():
			self.conn.start()

	def stop_thread(self):
		"""
		Closes the serial port. Joins the thread
		"""
		if self.conn.isRunning():
			self.conn.ser.close()
			self.conn.wait()

	def write(self, char: str):
		if self.conn.isRunning():
			self.conn.ser.write(char)

	def write_string(self, string: str):
		if self.conn.isRunning():
			string = bytes(string + "\n", "utf-8")
			self.conn.ser.write(string)




	def start_session(self):
		"""
		Retrieves and applies settings.
		Instantiates a fresh `SerialConnection`
		"""
		port = SERIAL_SETTINGS["port"]
		baudrate = SERIAL_SETTINGS["baudrate"]
		ser = serial.Serial(
			port=port,
			baudrate=baudrate,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		self.conn = SerialConnection(ser=ser)
		self.conn.rx.connect(lambda byte: self.rx.emit(byte))
		self.start_thread()
