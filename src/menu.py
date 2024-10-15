from qtstrap import *
import os


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
        self.port.setText("/dev/ttyUSB0")  # temporary
        self.connect_button = QPushButton(
            "Connect", clicked=self.handle_connect)
        self.disconnect_button = QPushButton(
            "Disconnect", clicked=self.handle_disconnect)
        self.cancel_button = QPushButton("Cancel", clicked=self.handle_cancel)

        self.center_on_parent()

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

    def center_on_parent(self):
        pass
        # parent = self.parent().parent()
        # if parent:
        # 	parent_geometry = parent.geometry()
        # 	dialog_geometry = self.geometry()

        # 	x = QApplication.primaryScreen().availableGeometry().x() // 2
        # 	y = QApplication.primaryScreen().availableGeometry().y() // 2

        # 	self.move(x, y)
        # 	print(f"Dialog centered on parent at: {x}, {y}")
        # 	print(f"Available screen geometry: {QApplication.primaryScreen().availableGeometry()}")

    def handle_connect(self):
        port = self.port.text()
        baudrate = int(self.baudrate.currentText())
        if port:
            settings = {"port": port, "baudrate": baudrate}
            self.serial_settings_signal.emit(settings)
            self.accept()

    def handle_disconnect(self):
        self.port.clear()
        self.disconnect_signal.emit()
        self.accept()

    def handle_cancel(self):
        self.port.clear()
        self.baudrate.setCurrentIndex(self.bauds.index("115200"))
        self.accept()


class AboutDialog(QDialog):
    """
    Read-only dialog.
    Just contains a logo and version info
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_path, "assets", "echologics_logo.png")

        with CVBoxLayout(self, align="center") as layout:
            with layout.hbox() as layout:
                image_label = QLabel(self)
                image_label.setPixmap(QPixmap(logo_path))
                layout.add(image_label)
            with layout.hbox() as layout:
                layout.add(QLabel("Echoterm Version 0.1.0"))


class Menu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.connection_dialog = ConnectionDialog(parent=self)
        self.about_dialog = AboutDialog(parent=self)

        file_menu = self.addMenu("File")

        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: self.about_dialog.exec_())
        file_menu.addAction(about_action)

        connect_action = QAction("Manage Connections", self)
        connect_action.triggered.connect(
            lambda: self.connection_dialog.exec_())
        file_menu.addAction(connect_action)

        self.clear_action = QAction("Clear", self)
        file_menu.addAction(self.clear_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        self.addMenu("Edit")
