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

        self.regex = QRegularExpressionValidator(QRegularExpression("[0-9 ]+"))

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1 = QLabel("n")
        self.left_group_box_layout.addWidget(self.variable_1,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setValidator(self.regex)
        self.variable_1_input.setPlaceholderText("Number Of Trials")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2 = QLabel("p")
        self.left_group_box_layout.addWidget(self.variable_2,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9./ ]+")))
        self.variable_2_input.setPlaceholderText("Probability Of Success")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

        self.variable_3 = QLabel("x")
        self.left_group_box_layout.addWidget(self.variable_3,2,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("Target Successes")
        self.left_group_box_layout.addWidget(self.variable_3_input,2,1)

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

        self.variable_1_info = QTextEdit("<b>Binomial Distribution:</b><br>"
                                        "A discrete probability distribution that measures the likelihood of getting exactly <b>x successes</b> in a fixed number of <b>n independent trials</b>.<br>"
                                        "<i>(e.g., calculating the probability of getting exactly 3 heads when flipping a fair coin 10 times.)</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("n")
        self.right_group_box_layout.addWidget(self.variable_1_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>n (Number of Trials):</b><br>"
                                        "The total number of identical and independent experiments or observations you are conducting.<br> "
                                        "<i>(e.g., flipping a coin 10 times &rarr; n = 10)</i>")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("p")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>p (Probability of Success):</b><br>"
                                        "The likelihood that a specific outcome (a 'success') occurs in a <b>single</b> trial. "
                                        "This value must always be between 0 and 1.<br>"
                                        "<i>(e.g., getting heads on a fair coin &rarr; p = 0.5)</i>")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)


        self.variable_4_info_label = QLabel("x")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b>x or k (Target Successes):</b><br>"
                                    "The exact number of successful outcomes you want to find the probability for. "
                                    "This must be a whole number between 0 and <i>n</i>.<br>"
                                    "<i>(e.g., wanting exactly 3 heads out of 10 flips &rarr; x = 3)</i>")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

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
                self.current_result = "<span style='color: #EF4444; font-size: 20px;'>P must be between 1 and 0!</span>"
        except (ValueError, ZeroDivisionError):
            pass
        return None

    def update_formula_display(self):
        self.variable_1_display = self.variable_1_input.text().strip() or "n"
        self.variable_2_display = "p"
        self.variable_3_display = self.variable_3_input.text().strip() or "x"

        self.variable_2 = self.parse_probability(self.variable_2_input.text().strip())

        if self.variable_2 is not None: self.variable_2_display = f"{self.variable_2:.5f}"

        
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" style="font-size: 32px; font-family: 'Times New Roman', serif;">
                <tr>
                    <td valign="middle">
                        <i>P(X = {self.variable_3_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="font-size: 50px; font-weight: 200;">
                        (
                    </td>
                    
                    <td valign="middle" align="center">
                        <table cellpadding="0" cellspacing="0" style="font-size: 30px;">
                            <tr><td align="center">{self.variable_1_display}</td></tr>
                            <tr><td align="center">{self.variable_3_display}</td></tr>
                        </table>
                    </td>
                    
                    <td valign="middle" style="font-size: 50px; font-weight: 200;">
                        )
                    </td>

                    <td valign="middle">
                        {self.variable_2_display}<sup>{self.variable_3_display}</sup>(1 - {self.variable_2_display})<sup>{self.variable_1_display} - {self.variable_3_display}</sup>
                    </td>

                    <td valign="middle">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            n = int(self.variable_1_display)
            x = int(self.variable_3_display)
            if x < 0 or x > n:
                self.current_result = "<span style='color: #F59E0B; font-size: 16px;'>'x' must be 0 to n!</span>"
            if n <= 0:
                self.current_result = "<span style='color: #F59E0B; font-size: 16px;'>'n' must be > 0!</span>"
            else:
                combination = math.comb(n,x)
                success_prob = self.variable_2 ** x
                failure_prob = (1 - self.variable_2) ** (n - x)
                result = combination * success_prob * failure_prob

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Div by Zero!</span>"
        except Exception:
             self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Error!</span>"

        self.update_formula_display()



        