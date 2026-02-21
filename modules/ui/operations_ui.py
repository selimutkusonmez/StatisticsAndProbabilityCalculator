import sys
import subprocess
from PyQt6.QtCore import Qt,QRegularExpression,QSize,pyqtSignal
from PyQt6.QtWidgets import (
     QApplication,QWidget,QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QGridLayout,QFrame,QTableWidget,QTableWidgetItem,QGroupBox,QComboBox,QMessageBox,QFileDialog,QListWidget,QTabWidget,QVBoxLayout,QStatusBar,QSizePolicy,QHBoxLayout)
from PyQt6.QtGui import QIcon,QPixmap,QIntValidator,QDoubleValidator,QRegularExpressionValidator,QKeyEvent,QPainter,QFontDatabase,QFont,QAction,QActionGroup

from config import JPG_PATH

class OperationsUI(QWidget):
     chosen_subject = pyqtSignal(str)

     def __init__(self):
          super().__init__()
          self.init_ui()
     
     def init_ui(self):
        
          #Layout created
          self.layout = QHBoxLayout()
          self.setLayout(self.layout)

          self.subjects_dict = {

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
                    ["Central Limit Theorem","Central Limit Theorem"],
                    ["Confidence Interval","Confidence Interval"],
                    ["Margin Of Error","Margin Of Error"],
                    ["Z Test","One-Tailed Z Test","Two-Tailed Z Test"],
                    ["t Test","One-Tailed t Test","Two-Tailed t Test","Single-Sample t Test","Independent Sample t Test","Paired Sample t test"],
                    ["Chi-Square Test","Chi-Square Test"],
                    ["ANOVA - Analysis Of Variance","ANOVA - Analysis Of Variance"],
                    ["Bayes","Bayes"],
               ],
               }
          
          self.subjects_list_1 = QListWidget()
          self.subjects_list_1.itemDoubleClicked.connect(self.subjects_list_1_item_double_clicked)
          self.layout.addWidget(self.subjects_list_1)

          for key in self.subjects_dict.keys():
               self.subjects_list_1.addItem(key)

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
          self.subjects_list_2.itemDoubleClicked.connect(self.subjects_list_2_item_double_clicked)
          self.layout.addWidget(self.subjects_list_2)

          self.current_subject = item.text()
          
          for i in self.subjects_dict[item.text()]:
               self.subjects_list_2.addItem(i[0])
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
          self.subjects_list_3.itemDoubleClicked.connect(self.subjects_list_3_item_double_clicked)
          self.layout.addWidget(self.subjects_list_3)

          for i in self.subjects_dict[self.current_subject][self.subjects_list_2.row(item)][1:]:
               self.subjects_list_3.addItem(i)
          self.chosen_subject.emit(item.text())

     def subjects_list_3_item_double_clicked(self,item):
          return

     

          
                    
               



