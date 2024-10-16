from qtstrap import *
from event_listener import wait_for
import io
import traceback


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
        output_buffer = io.StringIO()
        
        sys.stdout = output_buffer
        sys.stderr = output_buffer
        
        try:
            exec(script, globals())
            self.output_display.setPlainText(f"{output_buffer.getvalue()}")
        except Exception:
            error_message = traceback.format_exc()
            self.output_display.setPlainText(f"Error:\n{error_message}")
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            output_buffer.close()
