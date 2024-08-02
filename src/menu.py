from qtstrap import *


class ConnectDialog(QDialog):

	serial_settings = Signal(dict)

	def __init__(self, parent=None):
		super().__init__(parent=parent)

		self.setWindowTitle("Connection Settings")
		self.setGeometry(100, 100, 300, 200)

		self.bauds = [
			"9600", "19200", "38400", "57600", "115200"
		]
		self.baudrate = QComboBox()
		self.baudrate.addItems(self.bauds)
		self.baudrate.setCurrentIndex(self.bauds.index("115200"))

		self.port = QLineEdit()
		self.ok_button = QPushButton("Ok", clicked=self.handle_ok)
		self.cancel_button = QPushButton("Cancel", clicked=self.handle_cancel)

		with CVBoxLayout(self, align="left") as layout:
			with layout.hbox() as layout:
				layout.add(QLabel("Port:"))
				layout.add(self.port)
			with layout.hbox() as layout:
				layout.add(QLabel("Baudrate:"))
				layout.add(self.baudrate)
			with layout.hbox() as layout:
				layout.add(self.ok_button)
				layout.add(self.cancel_button)
	
	def handle_ok(self):
		port = self.port.text()
		baudrate = int(self.baudrate.currentText())
		if port:
			settings = {"port": port, "baudrate": baudrate}
			self.serial_settings.emit(settings)
			self.accept()

	def handle_cancel(self):
		self.port.clear()
		self.baudrate.setCurrentIndex(self.bauds.index("115200"))
		self.accept()


class Menu(QMenuBar):
	def __init__(self, parent=None):
		super().__init__(parent=parent)

		self.connect_dialog = ConnectDialog()
		
		file_menu = self.addMenu("File")

		connect_action = QAction("Connect", self)
		connect_action.triggered.connect(lambda: self.connect_dialog.exec_())
		file_menu.addAction(connect_action)

		quit_action = QAction("Quit", self)
		file_menu.addAction(quit_action)

		self.addMenu("Edit")

	