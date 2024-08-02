from qtstrap import *
from terminal_widget import TerminalWidget


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Echoterm")

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.term = TerminalWidget()

        with CVBoxLayout(widget) as layout:
            layout.add(self.term)