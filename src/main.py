from qtstrap import *
from main_window import MainWindow


class Application(BaseApplication):
    def __init__(self) -> None:
        super().__init__()
        self.window = MainWindow()
        self.window.show()


def run():
    app = Application()
    app.exec_()


if __name__ == "__main__":
    run()