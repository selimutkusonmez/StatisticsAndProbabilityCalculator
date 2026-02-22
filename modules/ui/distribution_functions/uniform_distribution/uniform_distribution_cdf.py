from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QComboBox,QListWidget,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QIcon,QIntValidator,QDoubleValidator,QRegularExpressionValidator
import math
import statistics

class OperationWidget(QWidget):
    def __init__(self,operation_name):
        super().__init__()
        self.operation_name = operation_name
        self.init_ui()

    def init_ui(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.current_result = "<i>Waiting...</i>"

        self.regex = QRegularExpressionValidator(QRegularExpression("[-0-9. ]+"))

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("x")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setValidator(self.regex)
        self.variable_1_input.setPlaceholderText("Z Score")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2_label = QLabel("a")
        self.variable_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_2_label,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Z Score")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

        self.variable_3_label = QLabel("b")
        self.variable_3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_3_label,2,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("Z Score")
        self.left_group_box_layout.addWidget(self.variable_3_input,2,1)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,3,0,1,2)

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

        self.variable_1_info_label = QLabel()
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>Continuous Uniform Distribution (CDF):</b><br>"
                                        "Represents the probability that a random variable X will take a value <b>less than or equal to x</b>.<br><br>"
                                        "<i>Visually, it calculates the area of the rectangle from the start point (a) up to your target value (x). "
                                        "Once x exceeds the upper bound (b), the total probability remains 1.</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("x")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b>x (Target):</b><br> The point up to which the area is calculated.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_2_info_label = QLabel("a")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,2,0)
        
        self.variable_2_info = QTextEdit("<b>a (Min):</b><br> Start of the distribution.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,2,1)


        self.variable_2_info_label = QLabel("b")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,3,0)
        
        self.variable_2_info = QTextEdit("<b>b (Max):</b><br> End of the distribution.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,3,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.textChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = self.variable_1_input.text().strip() or "x"
        self.variable_2_display = self.variable_2_input.text().strip() or "a"
        self.variable_3_display = self.variable_3_input.text().strip() or "b"

        try:
            self.variable_1 = float(self.variable_1_display)
            self.variable_2  = float(self.variable_2_display)
            self.variable_3  = float(self.variable_3_display)

            if self.variable_2 >= self.variable_3:
                self.current_result = "<span style='color: #EF4444; font-size: 20px;'>b > a !</span>"
            else:
                self.variable_1_display = f"{self.variable_1:.2f}"
                self.variable_2_display = f"{self.variable_2:.2f}"
                self.variable_3_display = f"{self.variable_3:.2f}"

        except ValueError:
            pass

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" style="font-size: 38px; font-family: 'Times New Roman', serif;">
                <tr>
                    <td valign="middle" style="padding-right: 10px;"><i>F({self.variable_1_display})</i> = </td>
                    
                    <td valign="middle" style="font-size: 200px; font-weight: lighter; padding-right: 15px; padding-bottom: 10px;">{{</td>

                    <td valign="middle">
                        <table cellpadding="4" cellspacing="0" style="font-size: 24px;">
                            <tr>
                                <td>0 ,</td>
                                <td style="padding-left: 20px;">{self.variable_1_display} &lt; {self.variable_2_display}</td>
                            </tr>
                            <tr>
                                <td valign="middle">
                                    <table cellpadding="0" cellspacing="0">
                                        <tr><td align="center" style="border-bottom: 2px solid currentColor;">{self.variable_1_display} &minus; {self.variable_2_display}</td></tr>
                                        <tr><td align="center">{self.variable_3_display} &minus; {self.variable_2_display}</td></tr>
                                    </table>
                                </td>
                                <td valign="middle" style="padding-left: 20px;">{self.variable_2_display} &le; {self.variable_1_display} &le; {self.variable_3_display}</td>
                            </tr>
                            <tr>
                                <td>1 ,</td>
                                <td style="padding-left: 20px;">{self.variable_1_display} &gt; {self.variable_3_display}</td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 30px;">= {self.current_result}</td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            if self.variable_2 <= self.variable_1 <= self.variable_3:
                result = (self.variable_1 - self.variable_2) / (self.variable_3 - self.variable_2)
                
            elif self.variable_1 < self.variable_2:
                result = 0.0
            else:
                result = 1.0

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Div by Zero!</span>"
        except Exception:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Error!</span>"

        self.update_formula_display()



        