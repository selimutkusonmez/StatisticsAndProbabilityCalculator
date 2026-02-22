from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QComboBox,QListWidget,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QIcon,QIntValidator,QDoubleValidator,QRegularExpressionValidator
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

        self.regex = QRegularExpressionValidator(QRegularExpression("[1-9 ]+"))

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("<i>&lambda;</i>")
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9./ ]+")))
        self.variable_1_input.setPlaceholderText("Number Of Trials")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2_label = QLabel("x")
        self.left_group_box_layout.addWidget(self.variable_2_label,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Probability Of Success")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

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

        self.right_group_box.setFixedWidth(300)

        self.variable_1_info_label = QLabel()
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>Poisson CDF (Cumulative Distribution Function):</b><br>"
                                        "Calculates the probability that a random variable X will take a value <b>less than or equal to</b> a specific value (x) in a fixed interval.<br><br>"
                                        "<i>(e.g., If &lambda; = 3, and x = 2, it calculates the total probability of exactly 0, PLUS exactly 1, PLUS exactly 2 occurrences.)</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("<i>&lambda;</i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>&lambda; (Lambda / Average Rate):</b><br>"
                                        "The average number of times the event occurs in the specified interval. "
                                        "This value must be greater than 0 (<b>&lambda; > 0</b>).")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("x")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>x (Maximum Target Events):</b><br>"
                                        "The upper limit of occurrences you want to find the cumulative probability for. "
                                        "Calculates P(X &le; x). This must be a whole number (<b>x &ge; 0</b>).")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        self.update_formula_display()

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
            if val > 0:
                return val
            else:
                self.current_result = "<span style='color: #EF4444; font-size: 20px;'>&lambda; must be greater than 0</span>"
        except (ValueError, ZeroDivisionError):
            pass
        return None

    def update_formula_display(self):
        self.variable_1_display = "<i>&lambda;</i>"
        self.variable_2_display = self.variable_2_input.text().strip() or "k"

        self.variable_1 = self.parse_probability(self.variable_1_input.text().strip())

        if self.variable_1 is not None: self.variable_1_display = f"{self.variable_1:.4f}"

        try:
            self.variable_2 = int(self.variable_2_input.text().strip())
            if self.variable_2 >= 0: self.variable_2_display = f"{self.variable_2}"
        except ValueError:
            self.variable_2_display = "k"

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" style="font-size: 32px; font-family: 'Times New Roman', serif;">
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        <i>P(X &le; {self.variable_2_display})</i> = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr><td align="center" style="font-size: 18px; padding-bottom: 2px;">{self.variable_2_display}</td></tr>
                            <tr><td align="center" style="font-size: 40px; line-height: 0.8;">&sum;</td></tr>
                            <tr><td align="center" style="font-size: 18px; padding-top: 8px;"><i>i=0</i></td></tr>
                        </table>
                    </td>
                    
                    <td valign="middle" style="padding-left: 10px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 28px;">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 10px 4px 10px;">
                                    {self.variable_1_display}<sup>i</sup> &middot; <i>e</i><sup>-{self.variable_1_display}</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 0px 10px;">
                                    i!
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 20px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            cdf_result = 0.0
            for k in range(self.variable_2 + 1):
                numerator = (self.variable_1 ** k) * math.exp(-self.variable_1)
                denominator = math.factorial(k)
                cdf_result += numerator / denominator

            result = min(cdf_result,1.0)

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Div by Zero!</span>"
        except Exception:
             self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Error!</span>"

        self.update_formula_display()



        