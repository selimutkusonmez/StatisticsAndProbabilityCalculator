import sys
import subprocess
from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import (
     QApplication,QWidget,QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QGridLayout,QFrame,QTableWidget,QTableWidgetItem,QGroupBox,QComboBox,QMessageBox,QFileDialog,QListWidget,QTabWidget,QVBoxLayout,QStatusBar,QSizePolicy,QHBoxLayout)
from PyQt6.QtGui import QIcon,QPixmap,QIntValidator,QDoubleValidator,QRegularExpressionValidator,QKeyEvent,QPainter,QFontDatabase,QFont,QAction,QActionGroup

from config import JPG_PATH

class OperationsUI(QWidget):
     def __init__(self):
          super().__init__()
          self.init_ui()
     
     def init_ui(self):
        
          #Layout created
          self.layout = QHBoxLayout()
          self.setLayout(self.layout)


          self.operations = {

               "Statistics" : [
                    ["Mean","Population Mean","Sample Mean"],
                    ["Variance","Population Variance","Sample Variance"],
                    ["Standard Deviation","Population Standard Deviation", "Sample Standard Deviation"],
                    ["Percentile","25th Percentile","50th Percentile","75th Percentile"],
                    ["Covariance","Population Covariance","Sample Covariance"],
                    ["Correlation","Correlation"],
               ],

               "Probability" : [
                    ["Addition Rule","Mutually Exclusive","Non-Mutually Exclusive"],
                    ["Multiplication Rule","Independent Event", "Dependent Events"],
               ],

               "Distribution Functions" : [
                    ["PMF","PMF"],
                    ["PDF","PDF"],
                    ["CDF","CDF"],
                    ["Bernoulli Distribution","Bernoulli Distribution"],
                    ["Binomial Distribution","Binomial Distribution"],
                    ["Poisson Distribution","PMF","CDF"],
                    ["Normal Distribution","PDF","CDF"],
                    ["Standard Normal Distribution","Standard Normal Distribution"],
                    ["Z Score","Z Score"],
                    ["Uniform Distribution","PMF","CDF"],
                    ["Log-Normal Distribution","PDF","CDF"],
                    ["Pareto Distribution","PDF","CDF"],
               ],

               "Hypothesis Tests" : [
                    ["Central Limit Theorem"],
                    ["Confidence Interval"],
                    ["Margin Of Error"],
                    ["Z Test","One-Tailed Z Test","Two-Tailed Z Test"],
                    ["t Test","One-Tailed t Test","Two-Tailed t Test","Single-Sample t Test","Independent Sample t Test","Paired Sample t test"],
                    ["Chi-Square Test"],
                    ["ANOVA - Analysis Of Variance"],
                    ["Bayes"],
               ],
               }
          
          self.operations_list = QListWidget()
          self.operations_list.itemDoubleClicked.connect(self.operation_list_item_double_clicked)
          self.layout.addWidget(self.operations_list)
          for key in self.operations.keys():
               self.operations_list.addItem(key)

     def operation_list_item_double_clicked(self,item):
          if hasattr(self, "operations_sub_sub_list"):
               try:
                    self.layout.removeWidget(self.operations_sub_sub_list)
                    self.operations_sub_sub_list.deleteLater()
                    del self.operations_sub_sub_list
               except :
                    pass
          
          if hasattr(self, "operations_sub_list"):
               try:
                    self.layout.removeWidget(self.operations_sub_list)
                    self.operations_sub_list.deleteLater()
                    del self.operations_sub_list
               except : 
                    pass
         
          self.operations_sub_list = QListWidget()
          self.operations_sub_list.itemDoubleClicked.connect(self.operations_sub_list_item_double_clicked)
          self.current_subject = item.text()
          self.layout.addWidget(self.operations_sub_list)
          for i in self.operations[item.text()]:
               self.operations_sub_list.addItem(i[0])

     def operations_sub_list_item_double_clicked(self,item):
          if hasattr(self, "operations_sub_sub_list"):
               try:
                    self.layout.removeWidget(self.operations_sub_sub_list)
                    self.operations_sub_sub_list.deleteLater()
                    del self.operations_sub_sub_list
               except :
                     pass
          
          self.operations_sub_sub_list = QListWidget()
          self.layout.addWidget(self.operations_sub_sub_list)
          for i in self.operations[self.current_subject][self.operations_sub_list.row(item)][1:]:
               self.operations_sub_sub_list.addItem(i)
          
                    
               



