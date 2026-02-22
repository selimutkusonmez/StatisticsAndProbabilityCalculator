import sys
from PyQt6.QtWidgets import QApplication

from modules.ui.main_ui import MainUI

class AppManager():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_ui = MainUI()
        
    def init_main_ui(self):
        self.main_ui.showMaximized()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    manager = AppManager()
    manager.init_main_ui()