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

        self.regex = QRegularExpressionValidator(QRegularExpression("[0-9./ ]+"))

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("P(A)")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setValidator(self.regex)
        self.variable_1_input.setPlaceholderText("a/b or a.b")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2_label = QLabel("P(B)")
        self.variable_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_2_label,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("c/d or c.d")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,2,0,1,2)

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

        self.variable_1_info_label = QLabel("<i>P(A &cup; B)</i>")
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>P(A &cup; B) (Probability of A Union B):</b><br>"
                                        "The probability that either event A occurs, event B occurs, or both occur. "
                                        "This represents the union of two events.<br>"
                                        "<i>Note (Addition Rule):</i> If events A and B are mutually exclusive (they cannot happen at the same time), "
                                        "then P(A &cup; B) = P(A) + P(B). If they can happen together, you must subtract the intersection: P(A &cap; B).")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("P(A)")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>P(A) (Probability of Event A):</b><br>"
                                        "The likelihood or chance that event A will occur.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("P(B)")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>P(B) (Probability of Event B):</b><br>"
                                        "The likelihood or chance that event B will occur.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        self.update_formula_display()
        self.left_hide = False
        self.right_hide = False

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)


    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()


    def parse_probability(self, text):
        if not text:
            return None
        try:
            parts = text.split("/")
            val = float(parts[0]) / float(parts[1]) if len(parts) == 2 else float(text)
            if 0.0 <= val <= 1.0:
                return val
            else:
                self.current_result = "<span style='color: #EF4444;'>P must be between 1 and 0!</span>"
        except (ValueError, ZeroDivisionError):
            pass
        return None
    
    def update_formula_display(self):
        self.variable_1_display = "P(A)"
        self.variable_2_display = "P(B)"

        self.variable_1 = self.parse_probability(self.variable_1_input.text().strip())
        self.variable_2 = self.parse_probability(self.variable_2_input.text().strip())

        if self.variable_1 is not None: self.variable_1_display = f"{self.variable_1:.2f}"
        if self.variable_2 is not None: self.variable_2_display = f"{self.variable_2:.2f}"

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        <i>P(A &cup; B)</i> = 
                    </td>
                    
                    <td valign="middle">
                        <td align="center";">
                            {self.variable_1_display} + {self.variable_2_display}
                        </td>
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
                result = self.variable_1 + self.variable_2
                if result > 1:
                    result = 1

                self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except (TypeError,ValueError):
            self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"

        except AttributeError:
             self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
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


        