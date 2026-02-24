import sys
import subprocess
import importlib
import os
from PyQt6.QtCore import Qt,QRegularExpression,QSize,pyqtSignal
from PyQt6.QtWidgets import (
     QApplication,QWidget,QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QGridLayout,QFrame,QTableWidget,QTableWidgetItem,QGroupBox,QComboBox,QMessageBox,QFileDialog,QListWidget,QTabWidget,QVBoxLayout,QStatusBar,QSizePolicy,QHBoxLayout,QListWidgetItem)
from PyQt6.QtGui import QIcon,QPixmap,QIntValidator,QDoubleValidator,QRegularExpressionValidator,QKeyEvent,QPainter,QFontDatabase,QFont,QAction,QActionGroup

from config import JPG_PATH

class OperationsUI(QWidget):
     chosen_subject = pyqtSignal(str)
     operation_signal = pyqtSignal(QWidget,str)

     def __init__(self):
          super().__init__()

          self.icons_dir = os.path.join(JPG_PATH,"icons")
          self.init_ui()

     def get_icon(self, name, sub_folder):
          safe_name = name.lower().replace(" ", "_") + ".png"
          icon_path = os.path.join(self.icons_dir, sub_folder, safe_name)
          
          if os.path.exists(icon_path):
               return QIcon(icon_path)
          else:
               return QIcon()
     
     def init_ui(self):
        
          #Layout created
          self.layout = QHBoxLayout()
          self.setLayout(self.layout)

          self.subjects_dict = {

               "Statistics" : [
                    ["Mean","Population Mean","Sample Mean"],
                    ["Variance","Population Variance","Sample Variance"],
                    ["Standard Deviation","Population Standard Deviation", "Sample Standard Deviation"],
                    ["Percentile","Percentile"],
                    ["Covariance","Population Covariance","Sample Covariance"],
                    ["Correlation","Correlation"],
               ],

               "Probability" : [
                    ["Addition Rule","Mutually Exclusive","Non Mutually Exclusive"],
                    ["Multiplication Rule","Independent Events", "Dependent Events"],
               ],

               "Distribution Functions" : [
                    ["Bernoulli Distribution","Bernoulli Distribution"],
                    ["Binomial Distribution","Binomial Distribution"],
                    ["Poisson Distribution","Poisson Distribution PMF","Poisson Distribution CDF"],
                    ["Normal Distribution","Normal Distribution PDF","Normal Distribution CDF"],
                    ["Standard Normal Distribution","Standard Normal Distribution"],
                    ["Uniform Distribution","Uniform Distribution PDF","Uniform Distribution CDF"],
                    ["Log Normal Distribution","Log Normal Distribution PDF","Log Normal Distribution CDF"],
                    ["Pareto Distribution","Pareto Distribution PDF","Pareto Distribution CDF"],
               ],

               "Hypothesis Tests" : [
                    ["Central Limit Theorem","Central Limit Theorem"],
                    ["Confidence Interval","Confidence Interval"],
                    ["Margin Of Error","Margin Of Error"],
                    ["Z Test","One Tailed Z Test","Two Tailed Z Test"],
                    ["t Test","One Tailed t Test","Two Tailed t Test","Single Sample t Test","Independent Sample t Test","Paired Sample t test"],
                    ["Chi Square Test","Chi Square Test"],
                    ["ANOVA","ANOVA"],
                    ["Bayes","Bayes"],
               ],
               }
          
          self.subjects_list_1 = QListWidget()
          self.subjects_list_1.setProperty("class","list")
          self.subjects_list_1.setIconSize(QSize(150,150))
          self.subjects_list_1.itemDoubleClicked.connect(self.subjects_list_1_item_double_clicked)
          self.layout.addWidget(self.subjects_list_1)

          for key in self.subjects_dict.keys():
               item = QListWidgetItem(key)
               icon = self.get_icon(key,"main_subjects")
               item.setIcon(icon)
               self.subjects_list_1.addItem(item)

     def subjects_list_1_item_double_clicked(self,item):
          if hasattr(self, "subjects_list_3"):
               try:
                    self.layout.removeWidget(self.subjects_list_3)
                    self.subjects_list_3.deleteLater()
                    del self.subjects_list_3
               except :
                    pass
          
          if hasattr(self, "subjects_list_2"):
               try:
                    self.layout.removeWidget(self.subjects_list_2)
                    self.subjects_list_2.deleteLater()
                    del self.subjects_list_2
               except : 
                    pass
         
          self.subjects_list_2 = QListWidget()
          self.subjects_list_2.setProperty("class","list")
          self.subjects_list_2.setIconSize(QSize(150,150))
          self.subjects_list_2.itemDoubleClicked.connect(self.subjects_list_2_item_double_clicked)
          self.layout.addWidget(self.subjects_list_2)

          self.main_subject = item.text()
          
          for i in self.subjects_dict[item.text()]:
               item = QListWidgetItem(i[0])
               icon = self.get_icon(i[0],"sub_subjects")
               item.setIcon(icon)
               self.subjects_list_2.addItem(item)
          self.chosen_subject.emit(item.text())

     def subjects_list_2_item_double_clicked(self,item):
          if hasattr(self, "subjects_list_3"):
               try:
                    self.layout.removeWidget(self.subjects_list_3)
                    self.subjects_list_3.deleteLater()
                    del self.subjects_list_3
               except :
                     pass
          
          self.subjects_list_3 = QListWidget()
          self.subjects_list_3.setProperty("class","list")
          self.subjects_list_3.setIconSize(QSize(150,150))
          self.subjects_list_3.itemDoubleClicked.connect(self.subjects_list_3_item_double_clicked)
          self.layout.addWidget(self.subjects_list_3)

          self.sub_subject = item.text()

          for i in self.subjects_dict[self.main_subject][self.subjects_list_2.row(item)][1:]:
               item = QListWidgetItem(i)
               icon = self.get_icon("operations","operations")
               item.setIcon(icon)
               self.subjects_list_3.addItem(item)
          self.chosen_subject.emit(item.text())

     def subjects_list_3_item_double_clicked(self,item):
          operation_name = item.text()
          main_folder = self.main_subject.lower().replace(" ","_")
          sub_folder = self.sub_subject.lower().replace(" ","_")
          file_name = operation_name.lower().replace(" ","_")
          
          module_path = f"modules.ui.{main_folder}.{sub_folder}.{file_name}"

          try:
               module = importlib.import_module(module_path)
               widget = module.OperationWidget(operation_name)

               self.operation_signal.emit(widget,operation_name)
          except Exception as e:
               self.chosen_subject.emit(str(e))


     

          
                    
               



