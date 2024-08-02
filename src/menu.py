from qtstrap import *


class ConnectionDialog(QDialog):

	serial_settings_signal = Signal(dict)
	disconnect_signal = Signal()

	def __init__(self, parent=None):
		super().__init__(parent=parent)

		self.setWindowTitle("Connection Settings")
		self.setGeometry(100, 100, 300, 200)

		self.bauds = ["9600", "19200", "38400", "57600", "115200"]
		self.baudrate = QComboBox()
		self.baudrate.addItems(self.bauds)
		self.baudrate.setCurrentIndex(self.bauds.index("115200"))

		self.port = QLineEdit()
		self.connect_button = QPushButton("Connect", clicked=self.handle_connect)
		self.disconnect_button = QPushButton("Disconnect", clicked=self.handle_disconnect)
		self.cancel_button = QPushButton("Cancel", clicked=self.handle_cancel)

		with CVBoxLayout(self, align="left") as layout:
			with layout.hbox() as layout:
				layout.add(QLabel("Port:"))
				layout.add(self.port)
			with layout.hbox() as layout:
				layout.add(QLabel("Baudrate:"))
				layout.add(self.baudrate)
			with layout.hbox() as layout:
				layout.add(self.connect_button)
				layout.add(self.disconnect_button)
				layout.add(self.cancel_button)
	
	def handle_connect(self):
		port = self.port.text()
		baudrate = int(self.baudrate.currentText())
		if port:
			settings = {"port": port, "baudrate": baudrate}
			self.serial_settings_signal.emit(settings)
			self.accept()

	def handle_disconnect(self):
		self.disconnect_signal.emit()
		self.accept()

	def handle_cancel(self):
		self.port.clear()
		self.baudrate.setCurrentIndex(self.bauds.index("115200"))
		self.accept()


class Menu(QMenuBar):
	def __init__(self, parent=None):
		super().__init__(parent=parent)

		self.connection_dialog = ConnectionDialog()
		
		file_menu = self.addMenu("File")

		connect_action = QAction("Manage Connections", self)
		connect_action.triggered.connect(lambda: self.connection_dialog.exec_())
		file_menu.addAction(connect_action)

		quit_action = QAction("Quit", self)
		file_menu.addAction(quit_action)

		self.addMenu("Edit")

	