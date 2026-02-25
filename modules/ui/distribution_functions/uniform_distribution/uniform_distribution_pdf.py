from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QTextEdit,QVBoxLayout,QHBoxLayout
from PyQt6.QtGui import QRegularExpressionValidator


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
        self.variable_1_input.setPlaceholderText("x")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2_label = QLabel("a")
        self.variable_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_2_label,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("a")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

        self.variable_3_label = QLabel("b")
        self.variable_3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_3_label,2,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("b")
        self.left_group_box_layout.addWidget(self.variable_3_input,2,1)

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

        self.variable_1_info = QTextEdit("<b>Continuous Uniform Distribution (PDF):</b><br>"
                                        "A probability distribution where all values within a specific range (from <i>a</i> to <i>b</i>) are equally likely to occur. "
                                        "The shape of its PDF is a flat rectangle.<br><br>"
                                        "<i>If the target value (x) is outside the bounds [a, b], the probability density is exactly 0.</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("x")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b>x (Target Value):</b><br>"
                                        "The specific value whose probability density you want to calculate.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_2_info_label = QLabel("a")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,2,0)
        
        self.variable_2_info = QTextEdit("<b>a (Lower Bound):</b><br>"
                                        "The minimum possible value in the distribution.<br><br>")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,2,1)


        self.variable_2_info_label = QLabel("b")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,3,0)
        
        self.variable_2_info = QTextEdit("<b>b (Upper Bound):</b><br>"
                                        "The maximum possible value in the distribution. Must be greater than 'a' (b > a).<br><br>")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,3,1)

        self.update_formula_display()
        self.left_hide = False
        self.right_hide = False
        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.textChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = "x"
        self.variable_2_display = "a"
        self.variable_3_display = "b"

        self.variable_1_raw = self.variable_1_input.text().strip()
        self.variable_2_raw = self.variable_2_input.text().strip()
        self.variable_3_raw = self.variable_3_input.text().strip()

        if not self.variable_1_raw :
            self.variable_1 = None
        else:
            try:
                self.variable_1 = float(self.variable_1_raw)
                self.variable_1_display = f"{self.variable_1:.1f}"
            except:
                pass

        if not self.variable_2_raw:
            self.variable_2 = None
        else:
            try:
                self.variable_2 = float(self.variable_2_raw)
                self.variable_2_display = f"{self.variable_2:.1f}"
            except:
                pass

        if not self.variable_3_raw:
            self.variable_3 = None
        else:
            try:
                self.variable_3 = float(self.variable_3_raw)
                self.variable_3_display = f"{self.variable_3:.1f}"
            except:
                pass

        try:
            float(self.variable_2_raw)
            float(self.variable_3_raw)
            if self.variable_2 >= self.variable_3:
                self.current_result = "<span style='color: #EF4444;'>b must be &gt; a!</span>" 

        except ValueError:
            pass

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        <i>f({self.variable_1_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="font-size: 150px; font-weight: lighter; padding-bottom: 8px;">
                        {{
                    </td>

                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0" style="font-size: 32px;">
                            <tr>
                                <td valign="middle" align="center">
                                    <table cellpadding="0" cellspacing="0">
                                        <tr><td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 5px 2px 5px;">1</td></tr>
                                        <tr><td align="center" style="padding: 2px 5px 0px 5px;">{self.variable_3_display} &minus; {self.variable_2_display}</td></tr>
                                    </table>
                                </td>
                                <td valign="middle">,</td>
                                <td valign="middle" style="padding-left: 20px;">
                                    {self.variable_2_display} &le; {self.variable_1_display} &le; {self.variable_3_display}
                                </td>
                            </tr>
                            <tr>
                                <td valign="middle" align="center">0</td>
                                <td valign="middle">,</td>
                                <td valign="middle" style="padding-left: 20px;">
                                    other cases
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 35px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            if self.variable_2 <= self.variable_1 <= self.variable_3:
                result = 1 / (self.variable_3 - self.variable_2)
            else:
                result = 0.0

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444;'>Div by Zero!</span>"
        except TypeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
        except Exception:
            self.current_result = "<span style='color: #EF4444;'>Error!</span>"

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


        