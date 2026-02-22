from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QComboBox,QListWidget,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QIcon,QIntValidator,QDoubleValidator,QRegularExpressionValidator

class OperationWidget(QWidget):
    def __init__(self,operation_name):
        super().__init__()
        self.operation_name = operation_name
        self.init_ui()

    def init_ui(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.current_result = "<i>Waiting...</i>"

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(180)

        self.variable_1_label = QLabel("Data 1")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0)

        self.variable_2_label = QLabel("Data 2")
        self.variable_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_2_label,2,0)

        self.variable_2_input = QTextEdit()
        self.variable_2_input.setPlaceholderText("Seperated with comma")
        self.left_group_box_layout.addWidget(self.variable_2_input,3,0)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,4,0,1,2)

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

        self.right_group_box.setFixedWidth(250)

        self.variable_1_info_label = QLabel("&sigma;<sub>XY</sub>")
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>Cov(X,Y) (Covariance):</b><br>"
                                        "A statistical measure that shows the directional relationship between two random variables. "
                                        "It indicates how much two variables change together.<br><br>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("<i><b>&mu;<sub>X</sub></b></i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>&mu;<sub>X</sub> (Population Mean):</b> The average value of all observations in the entire population.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("<i><b>&mu;<sub>Y</sub></b></i>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>&mu;<sub>Y</sub> (Population Mean):</b> The average value of all observations in the entire population.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        self.variable_4_info_label = QLabel("N")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b>N (Population Size):</b> The total number of members or data points in the population.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)


    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()


    def update_formula_display(self):
        raw_text_1 = self.variable_1_input.toPlainText().strip()
        raw_text_2 = self.variable_2_input.toPlainText().strip()

        self.variable_1_display = "&mu;<sub>X</sub>"
        self.variable_2_display = "N"
        self.variable_3_display = "&mu;<sub>Y</sub>"
        self.variable_4_display = "N"

        if not raw_text_1 or not raw_text_2:
             pass
            
        else : 
            try:
                self.data_1 = [float(x.strip()) for x in raw_text_1.split(",") if x.strip()]
                self.variable_2 = len(self.data_1)
                
                

                self.data_2 = [float(x.strip()) for x in raw_text_2.split(",") if x.strip()]
                self.variable_4 = len(self.data_2)
                

                if self.variable_2 == 0 or self.variable_4 == 0 :
                     raise ZeroDivisionError
                
                if self.variable_2 != self.variable_4:
                     self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Dataset Length!</span>"

                else:
                    self.variable_2_display = self.variable_2
                    self.variable_1 = sum(self.data_1) / self.variable_2 
                    self.variable_3 = sum(self.data_2) / self.variable_4 
                    self.variable_1_display = f"{self.variable_1:.2f}"
                    self.variable_3_display = f"{self.variable_3:.2f}"

                
            except ValueError:
                self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"

            except ZeroDivisionError:
                pass


    
            
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        <i>&sigma;<sub>XY</sub></i> = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 8px;">
                                    &Sigma;<sub>i</sub><sup>{self.variable_2_display}</sup>(X<sub>i</sub> - {self.variable_1_display})(Y<sub>i</sub> - {self.variable_3_display})
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 8px 0px 8px;">
                                    {self.variable_2_display}
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 10px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
            """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
                result = sum((x - self.variable_1) * (y - self.variable_3) for x, y in zip(self.data_1, self.data_2))/self.variable_2

                self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except TypeError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"

        except AttributeError:
             self.current_result = "<span style='color: #EF4444; font-size: 20px;'>No Data!</span>"
        self.update_formula_display()



        