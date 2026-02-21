import sys
import subprocess
from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import (
     QApplication,QWidget,QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QGridLayout,QFrame,QTableWidget,QTableWidgetItem,QGroupBox,QComboBox,QMessageBox,QFileDialog,QListWidget,QTabWidget,QVBoxLayout,QStatusBar,QSizePolicy,QHBoxLayout)
from PyQt6.QtGui import QIcon,QPixmap,QIntValidator,QDoubleValidator,QRegularExpressionValidator,QKeyEvent,QPainter,QFontDatabase,QFont,QAction,QActionGroup

from modules.ui.operations_ui import OperationsUI
from modules.logic.style_reader.style_reader import read_style


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.operations_ui = OperationsUI()
        self.operations_ui.setProperty("class","operations_ui")
        self.init_ui()
        self.light_theme_action_function()

    def init_ui(self):

        self.setFixedSize(800,550)


        #Central Widget created
        self.central_widget = QTabWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.central_widget.addTab(self.operations_ui,"Operations")

        #Layout created and connected
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        #StatusBar
        self.setStatusBar(QStatusBar())

        #MenuBar created
        menu_bar = self.menuBar()

        #File Menu
        file_menu = menu_bar.addMenu("File")
        restart_app_action = QAction("Restart App",self)
        restart_app_action.setShortcut("Ctrl+R")
        restart_app_action.triggered.connect(self.restart_app_action_function)
        file_menu.addAction(restart_app_action)

        #Settings Menu
        settings_menu = menu_bar.addMenu("Settings")
        theme_menu = settings_menu.addMenu("Theme")
        theme_action_group = QActionGroup(self)

        #Light Theme
        light_theme_action = QAction("Light Theme")
        light_theme_action.setShortcut("Ctrl+L")
        light_theme_action.setCheckable(True)
        light_theme_action.setChecked(True)
        theme_menu.addAction(light_theme_action)
        theme_action_group.addAction(light_theme_action)
        light_theme_action.triggered.connect(self.light_theme_action_function)

        #Dark Theme
        dark_theme_action = QAction("Dark Theme")
        dark_theme_action.setShortcut("Ctrl+D")
        dark_theme_action.setCheckable(True)
        theme_menu.addAction(dark_theme_action)
        theme_action_group.addAction(dark_theme_action)
        dark_theme_action.triggered.connect(self.dark_theme_action_function)

        self.operations_ui.chosen_subject.connect(self.chosen_subject)


    def restart_app_action_function(self):
            QApplication.quit()
            subprocess.Popen([sys.executable, *sys.argv])

    def light_theme_action_function(self):
        self.setStyleSheet(read_style("main_ui_light_theme.qss"))

    def dark_theme_action_function(self):
        self.setStyleSheet(read_style("main_ui_dark_theme.qss"))
    
    def chosen_subject(self,chosen_subject):
         self.statusBar().showMessage(chosen_subject)
