from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QComboBox,QListWidget,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QIcon,QIntValidator,QDoubleValidator,QRegularExpressionValidator
import math
import statistics
from scipy import stats

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

        self.variable_2_label = QLabel("P(B|A)")
        self.left_group_box_layout.addWidget(self.variable_2_label,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("c/d or c.d")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

        self.variable_3_label = QLabel("P(B)")
        self.left_group_box_layout.addWidget(self.variable_3_label,2,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("e/f or e.f")
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

        self.right_group_box.setFixedWidth(375)

        self.variable_1_info_label = QLabel()
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>Bayes' Theorem:</b><br>"
                                        "A mathematical formula for updating the probability of a hypothesis (A) when given new evidence (B).")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("<b>P(A)</b>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b>P(A) (Prior Probability):</b><br>"
                                        "Your initial belief or the baseline probability of event A happening before any new evidence is considered.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("<b>P(B|A)</b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>P(B|A) (Likelihood):</b><br>"
                                        "The probability of observing the evidence (B) given that the hypothesis (A) is actually true.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)
        
        self.variable_4_info_label = QLabel("<b>P(B)</b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b>P(B) (Marginal Likelihood):</b><br>"
                                        "The total probability of observing the evidence (B) under all possible conditions.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.variable_5_info_label = QLabel("<b>P(A|B)</b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("<b>P(A|B) (Posterior Probability):</b><br>"
                                        "The updated probability of event A being true after observing the new evidence B. This is the result.")
        self.variable_5_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_5_info,4,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.textChanged.connect(self.reset_and_update_display)

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
        self.variable_2_display = "P(B|A)"
        self.variable_3_display = "P(B)"

        self.variable_1 = self.parse_probability(self.variable_1_input.text().strip())
        self.variable_2 = self.parse_probability(self.variable_2_input.text().strip())
        self.variable_3 = self.parse_probability(self.variable_3_input.text().strip())

        if self.variable_1 is not None: self.variable_1_display = f"{self.variable_1:.2f}"
        if self.variable_2 is not None: self.variable_2_display = f"{self.variable_2:.2f}"
        if self.variable_3 is not None: self.variable_3_display = f"{self.variable_3:.2f}"


        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        P(A|B) = 
                    </td>
                    <td align="center" valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                    {self.variable_2_display} &middot; {self.variable_1_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 6px 10px 0 10px;">
                                    {self.variable_3_display}
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td valign="middle" style="padding-left: 20px;">
                        = 
                    </td>
                    <td valign="middle" style="padding-left: 10px; line-height: 1.2;">
                        {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:   
            result = (self.variable_2 * self.variable_1) / self.variable_3

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.3f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444;'>P(B) &gt; 0!</span>"
        except TypeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
        except Exception:
            self.current_result = "<span style='color: #EF4444;'>Error!</span>"

        self.update_formula_display()
