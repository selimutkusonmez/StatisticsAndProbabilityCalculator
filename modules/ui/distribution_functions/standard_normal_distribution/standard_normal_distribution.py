from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QTextEdit,QVBoxLayout,QHBoxLayout
from PyQt6.QtGui import QRegularExpressionValidator
import math

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

        self.variable_1_label = QLabel("Z Score")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setValidator(self.regex)
        self.variable_1_input.setPlaceholderText("Z Score")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,3,0,1,2)

        #Middle GroupBox
        self.middle_group_box = QGroupBox()
        self.middle_group_box_layout = QVBoxLayout()
        self.middle_group_box.setLayout(self.middle_group_box_layout)
        self.layout.addWidget(self.middle_group_box,0,1)

        self.operation_name = QLabel(self.operation_name)
        self.operation_name.setObjectName("operation_name")
        self.operation_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_group_box_layout.addWidget(self.operation_name)
        self.middle_group_box_layout.addSpacing(30)
        self.middle_group_box_layout.addStretch()

        self.dynamic_formula = QLabel()
        self.dynamic_formula.setObjectName("dynamic_formula")
        self.dynamic_formula.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_group_box_layout.addWidget(self.dynamic_formula)

        self.middle_group_box_layout.addStretch()

        self.top_group_box = QGroupBox()
        self.top_group_box.setStyleSheet("""border:none;""")
        self.top_group_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.top_group_box_layout = QHBoxLayout()
        self.top_group_box.setLayout(self.top_group_box_layout)
        self.middle_group_box_layout.addWidget(self.top_group_box)

        self.hide_left_button = QPushButton("Hide Left")
        self.hide_left_button.setFixedWidth(150)
        self.hide_left_button.clicked.connect(self.hide_left_button_funtion)
        self.top_group_box_layout.addWidget(self.hide_left_button)
        self.top_group_box_layout.addStretch()

        self.hide_right_button = QPushButton("Hide Right")
        self.hide_right_button.setFixedWidth(150)
        self.hide_right_button.clicked.connect(self.hide_right_button_function)
        self.top_group_box_layout.addWidget(self.hide_right_button)

        #Right GroupBox
        self.right_group_box = QGroupBox()
        self.right_group_box_layout = QGridLayout()
        self.right_group_box.setLayout(self.right_group_box_layout)
        self.layout.addWidget(self.right_group_box,0,2)

        self.right_group_box.setFixedWidth(300)

        self.variable_1_info_label = QLabel()
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>Standard Normal Distribution:</b><br>"
                                        "A special case of the normal distribution where the <b>mean (&mu;) is 0</b> and the <b>standard deviation (&sigma;) is 1</b>.<br><br>"
                                        "<i>Because &mu;=0 and &sigma;=1, the complex normal formula simplifies elegantly, allowing us to find probabilities using only the Z-score.</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("Z")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b>z (Z-Score / Standard Score):</b><br>"
                                        "Represents how many standard deviations a value is from the mean. "
                                        "It can be positive (above average), negative (below average), or zero (exactly average).")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.update_formula_display()
        self.left_hide = False
        self.right_hide = False
        self.variable_1_input.textChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = self.variable_1_input.text().strip() or "z"

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 20px;">
                        <i>f({self.variable_1_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="padding-right: 10px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 36px;">
                            <tr>
                                <td align="center" style="border-bottom: 3px solid currentColor; padding: 0px 10px 4px 10px;">
                                    1
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 0px 10px;">
                                    &radic;<span style="text-decoration: overline;">2&pi;</span>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 5px;">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td valign="center" style="font-size: 51px; padding-right: 0px;">
                                    <i>e</i>
                                </td>
                                <td valign="top" style="padding-bottom: 28px; padding-left: 2px;">
                                    <table cellpadding="0" cellspacing="0" style="font-size: 30px;">
                                        <tr>
                                            <td rowspan="2" valign="middle" style="padding-right: 4px; font-size: 25px;">
                                                &minus;
                                            </td>
                                            <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 2px 1px 2px;">
                                                {self.variable_1_display}<sup>2</sup>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding: 1px 2px 0px 2px;">
                                                2
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 25px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            result = (1 / math.sqrt(2 * math.pi)) * (math.e ** (-(float(self.variable_1_display)**2)/2))

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444; '>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444; '>Div by Zero!</span>"
        except Exception:
             self.current_result = "<span style='color: #EF4444; '>Error!</span>"

        self.update_formula_display()

    def hide_left_button_funtion(self):
        if not self.left_hide:
            self.left_group_box.hide()
            self.left_hide = True
        else:
            self.left_group_box.show()
            self.left_hide = False

    def hide_right_button_function(self):
        if not self.right_hide:
            self.right_group_box.hide()
            self.right_hide = True
        else:
            self.right_group_box.show()
            self.right_hide = False


        