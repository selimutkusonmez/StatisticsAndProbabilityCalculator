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

        self.regex = QRegularExpressionValidator(QRegularExpression("[0-9. ]+"))

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("CL")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setPlaceholderText("Confidence Interval")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2_label = QLabel("<i>&sigma;</i>")
        self.left_group_box_layout.addWidget(self.variable_2_label,1,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Population STD")
        self.left_group_box_layout.addWidget(self.variable_2_input,1,1)

        self.variable_3_label = QLabel("n")
        self.left_group_box_layout.addWidget(self.variable_3_label,2,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9 ]+")))
        self.variable_3_input.setPlaceholderText("Sample Size")
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

        self.variable_1_info = QTextEdit("<b>Margin of Error (ME):</b>"
                                        "The maximum expected difference between the true population parameter and the sample estimate."
                                        "It reflects the uncertainty in your sample statistic.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("Z")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("The standard score associated with your chosen confidence level (e.g., Z ≈ 1.96 for 95% confidence)."
                                        "It determines how wide the interval must be to achieve that level of certainty.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        
        self.variable_3_info_label = QLabel("<b>σ</b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("The true variance of the underlying population." \
                                        "It measures the spread of the data.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        self.variable_4_info_label = QLabel("<b>n</b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("The true standard deviation of the entire population."
                                        "It measures the amount of variation or dispersion in the data."
                                        "A higher σ means the data is more spread out, which results in a wider, less precise confidence interval.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.textChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = "Z"
        self.variable_2_display = "<i>&sigma;</i>"
        self.variable_3_display = "n"

        self.variable_1_raw = self.variable_1_input.text().strip()
        self.variable_2_raw = self.variable_2_input.text().strip()
        self.variable_3_raw = self.variable_3_input.text().strip()

        if not self.variable_1_raw:
            self.variable_1 = None
        else:
            self.variable_1 = float(self.variable_1_raw)
            if self.variable_1 < 0 or self.variable_1 > 100:
                self.current_result = "<span style='color: #EF4444;'>Invalid CL Input!</span>"
            else:
                try:
                    alpha = 1 - (self.variable_1 / 100)
                    area = 1 - (alpha / 2)
                    self.variable_1 = statistics.NormalDist().inv_cdf(area)
                    self.variable_1_display = f"{self.variable_1:.2f}"
                except statistics.StatisticsError:
                    self.current_result = "<span style='color: #EF4444;'>Invalid CL Input!</span>"

        if not self.variable_2_raw:
            self.variable_2 = None
        else:
            self.variable_2_display = float(self.variable_2_raw)

        if not self.variable_3_raw:
            self.variable_3 = None
        else:
            self.variable_3_display = float(self.variable_3_raw)

            


        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        ME = 
                    </td>
                    
                    <td valign="middle" style="padding-right: 10px;">
                        {self.variable_1_display}<sup>*</sup>
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                    {self.variable_2_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 5px 10px;">
                                    &radic;{self.variable_3_display}
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
            self.variable_2 = float(self.variable_2_display)
            self.variable_3 = float(self.variable_3_display)
            margin_of_error = self.variable_1 * (self.variable_2 / math.sqrt(self.variable_3))
            result = margin_of_error

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.3f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444;'>Div by Zero!</span>"
        except TypeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
        except Exception:
            self.current_result = "<span style='color: #EF4444;'>Error!</span>"

        self.update_formula_display()



        