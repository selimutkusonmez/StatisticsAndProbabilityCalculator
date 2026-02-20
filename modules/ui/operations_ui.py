import sys
import subprocess
from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import (
     QApplication,QWidget,QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QGridLayout,QFrame,QTableWidget,QTableWidgetItem,QGroupBox,QComboBox,QMessageBox,QFileDialog,QListWidget,QTabWidget,QVBoxLayout,QStatusBar,QSizePolicy,QHBoxLayout)
from PyQt6.QtGui import QIcon,QPixmap,QIntValidator,QDoubleValidator,QRegularExpressionValidator,QKeyEvent,QPainter,QFontDatabase,QFont,QAction,QActionGroup

class OperationsUI(QWidget):
     def __init__(self):
          super().__init__()
          self.init_ui()
     
     def init_ui(self):
        
          #Layout created
          self.layout = QGridLayout()
          self.setLayout(self.layout)
        
          #Groupbox and Groupbox_Layout Ccreated and connected
          self.operations_groupbox = QGroupBox()
          self.operations_groupbox_layout = QGridLayout()
          self.operations_groupbox.setLayout(self.operations_groupbox_layout)

          #Groupbox added to the layout
          self.layout.addWidget(self.operations_groupbox)

          operations = {

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
                    ["PMF",],
                    ["PDF",],
                    ["CDF",],
                    ["Bernoulli Distribution",],
                    ["Binomial Distribution",],
                    ["Poisson Distribution","PMF","CDF"],
                    ["Normal Distribution","PDF","CDF"],
                    ["Standard Normal Distribution",],
                    ["Z Score",],
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
          self.operations_groupbox_layout.addWidget(self.operations_list,0,0)
          for key,val in operations.items():
               print(key)
               self.operations_list.addItem(key)

