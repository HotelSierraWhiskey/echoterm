from qtstrap import *
from event_listener import wait_for, WorkerSignals
import io
import traceback
from threading import Thread


class Worker(QThread):

	finished = Signal()

	def __init__(self, script):
		super().__init__()

	def run(self):
		output_buffer = io.StringIO()
		sys.stdout = output_buffer
		sys.stderr = output_buffer

		try:
			exec(self.script, globals())
			output = output_buffer.getvalue()
			# self.signals.output_ready.emit(output)
		except Exception:
			error_message = traceback.format_exc()
			# self.signals.error_occurred.emit(error_message)
		finally:
			sys.stdout = sys.__stdout__
			sys.stderr = sys.__stderr__
			output_buffer.close()
			self.deleteLater()
		
		self.finished.emit()


class CodeEditor(QWidget):
	def __init__(self):
		super().__init__()

		monospace_font = QFont("Courier", 10)

		self.code_editor = QPlainTextEdit()
		self.code_editor.setPlaceholderText("Write your script here...")
		self.code_editor.setFont(monospace_font)

		self.run_button = QPushButton("Run")
		self.run_button.clicked.connect(self.run)

		self.output_display = QPlainTextEdit()
		self.output_display.setReadOnly(True)
		self.output_display.setFont(monospace_font)

		self.worker_signals = WorkerSignals()

		globals()["wait_for"] = wait_for

		with CVBoxLayout(self) as layout:
			with layout.hbox(align="right") as layout:
				layout.add(self.code_editor)
			with layout.hbox(align="right") as layout:
				layout.add(self.output_display)
			with layout.hbox(align="right") as layout:
				layout.add(self.run_button)

	def run(self):
		script = self.code_editor.toPlainText()
		worker = Worker(script, self.worker_signals)
		# worker.finished.connect(worker.deleteLater)
		worker.start()