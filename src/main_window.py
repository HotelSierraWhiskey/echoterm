from qtstrap import *
from terminal_widget import TerminalWidget
from code_editor_widget import CodeEditor


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Echoterm")

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.term = TerminalWidget()
        self.code_editor = CodeEditor()

        with CHBoxLayout(widget) as layout:
            with layout.hbox(align="right") as layout:
                layout.add(self.code_editor)
            with layout.hbox(align="right") as layout:
                layout.add(self.term)