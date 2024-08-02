from qtstrap import *
import serial


class SerialConnection(QThread):
	"""
	The main serial interface.

	This runs a listener thread, forwarding received data to a `SerialManager`.
	Data transmission is handled by top level widgets via the `Serial` instance 
	member.
	"""

	rx = Signal(str)

	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self._is_running = True
		self.mutex = QMutex()
		self.ser = None

	def run(self):
		while True:
			if self.ser:
				byte = self.ser.read()
				char = byte.decode()
				self.rx.emit(char)
				
				self.mutex.lock()
				if not self._is_running:
					self.mutex.unlock()
					break
				self.mutex.unlock()

	def stop(self):
		self.mutex.lock()
		self._is_running = False
		self.mutex.unlock()


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
		if not self.conn.isRunning():
			self.conn.start()

	def stop_thread(self):
		if self.conn.isRunning():
			self.conn.stop()
			self.conn.wait()

	def apply_settings(self, settings):
		port = settings["port"]
		baudrate = settings["baudrate"]
		ser = serial.Serial(
			port=port,
			baudrate=baudrate,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		self.conn = SerialConnection()
		self.conn.ser = ser
		self.conn.rx.connect(lambda byte: self.rx.emit(byte))
