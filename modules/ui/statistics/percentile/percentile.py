from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QComboBox,QListWidget,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QIcon,QIntValidator,QDoubleValidator,QRegularExpressionValidator
import numpy as np

class OperationWidget(QWidget):
    def __init__(self,operation_name):
        super().__init__()
        self.operation_name = operation_name
        self.init_ui()

    def init_ui(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0)

        #Middle GroupBox
        self.middle_group_box = QGroupBox()
        self.middle_group_box_layout = QVBoxLayout()
        self.middle_group_box.setLayout(self.middle_group_box_layout)
        self.layout.addWidget(self.middle_group_box,0,1)
        self.middle_group_box_layout.addStretch()

        self.operation_name = QLabel(self.operation_name)
        self.operation_name.setObjectName("operation_name")
        self.operation_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_group_box_layout.addWidget(self.operation_name)
        self.middle_group_box_layout.addSpacing(30)

        self.dynamic_formula = QLabel()
        self.dynamic_formula.setObjectName("dynamic_formula")
        self.dynamic_formula.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_group_box_layout.addWidget(self.dynamic_formula)

        self.middle_group_box_layout.addStretch()

        #Right GroupBox
        self.right_group_box = QGroupBox()
        self.right_group_box_layout = QGridLayout()
        self.right_group_box.setLayout(self.right_group_box_layout)
        self.layout.addWidget(self.right_group_box,0,2)

        self.right_group_box.setFixedWidth(300)

        self.variable_1_info_label = QLabel("25th")
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>25th Percentile:</b><br>"
                                        "The value below which 25% of the data falls. It represents the lower 'quarter' of the dataset.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("50th")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>50th Percentile:</b><br>"
                                        "The middle value of the dataset. 50% of the data points are below this value and 50% are above it.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("75th")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>75th Percentile:</b><br>"
                                        "The value below which 75% of the data falls. It marks the boundary for the upper 25% of the dataset.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)


    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()


    def update_formula_display(self):
            
        raw_text = self.variable_1_input.toPlainText().strip()
        if not raw_text:
                self.variable_1 = "<i>Waiting...</i>"
                self.variable_2 = "<i>Waiting...</i>"
                self.variable_3 = "<i>Waiting...</i>"
            
        else : 
            try:
                self.data = [float(x.strip()) for x in raw_text.split(",") if x.strip()]
                self.variable_1 = np.percentile(self.data, 25)
                self.variable_2 = np.percentile(self.data, 50)
                self.variable_3 = np.percentile(self.data, 75)

            except ValueError:
                self.variable_1 = "<span style='color: #EF4444;'>Invalid Input!</span>"
                self.variable_2 = "<span style='color: #EF4444;'>Invalid Input!</span>"
                self.variable_3 = "<span style='color: #EF4444;'>Invalid Input!</span>"
    
            
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="1">
                <tr>
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td>
                                    25th Percentile : {self.variable_1}
                                    <br>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    50h Percentile : {self.variable_2}
                                    <br>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    75th Percentile : {self.variable_3}
                                    <br>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            """
        self.dynamic_formula.setText(html_formul)




        