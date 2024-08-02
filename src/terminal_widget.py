from qtstrap import *
from menu import Menu
from serial_manager import SerialManager


class TerminalEdit(QPlainTextEdit):
	"""
	This is the text-related component of the terminal interface.
	It's responsible for processing keypresses and characters
	received from the serial connection.
	"""

	tx = Signal(bytes)

	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setFont(QFont("Courier", 16))
		self.setStyleSheet("background-color: black; color: #00FF00;")
		self.setCursorWidth(10)
		self.setFont("Courier")

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
			self.tx.emit(b"\n")
		elif event.key() == Qt.Key_Escape:
			self.tx.emit(b"\x1b")
		else:
			byte = bytes(event.text().encode('utf-8'))
			self.tx.emit(byte)

	def write_char(self, char):
		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.End)
		cursor.insertText(char)
		self.setTextCursor(cursor)


class TerminalWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)

		self.serial_manager = SerialManager()
		self.serial_manager.rx.connect(lambda char: self.terminal_edit.write_char(char))

		self.menu = Menu()
		self.menu.connection_dialog.serial_settings_signal.connect(lambda settings: self.serial_manager.start_session(settings))
		self.menu.connection_dialog.disconnect_signal.connect(self.serial_manager.stop_thread)

		self.terminal_edit = TerminalEdit()
		self.terminal_edit.tx.connect(lambda char: self.serial_manager.write(char))

		self.clear_button = QPushButton(text="Clear", clicked=self.terminal_edit.clear)

		with CVBoxLayout(self) as layout:
			with layout.hbox() as layout:
				layout.add(self.menu)
			with layout.hbox() as layout:
				layout.add(self.terminal_edit)
			with layout.hbox() as layout:
				layout.add(self.clear_button)