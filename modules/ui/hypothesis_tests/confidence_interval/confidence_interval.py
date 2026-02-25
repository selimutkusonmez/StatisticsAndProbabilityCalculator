from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QTextEdit,QVBoxLayout,QHBoxLayout
from PyQt6.QtGui import QRegularExpressionValidator
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

        self.variable_1_label = QLabel("Sample Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0,1,2)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0,1,2)

        self.variable_2_label = QLabel("<i>&sigma;</i>")
        self.left_group_box_layout.addWidget(self.variable_2_label,2,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Population STD")
        self.left_group_box_layout.addWidget(self.variable_2_input,2,1)

        self.variable_3_label = QLabel("CL")
        self.left_group_box_layout.addWidget(self.variable_3_label,3,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9 ]+")))
        self.variable_3_input.setPlaceholderText("99 For %99")
        self.left_group_box_layout.addWidget(self.variable_3_input,3,1)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,4,0,1,2)

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

        self.variable_1_info = QTextEdit("<b>Confidence Interval (CI):</b>"
                                        "A range of values, derived from sample statistics,that is likely to contain the true population parameter.<br>"
                                        "For example, a 95% CI means if you repeat the sampling process, 95% of the calculated intervals will contain the true population mean.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("<i>X̄</i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("The average of your sample data. It serves as the exact center point (point estimate) of your confidence interval.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("Z")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("The standard score associated with your chosen confidence level (e.g., Z ≈ 1.96 for 95% confidence)."
                                        "It determines how wide the interval must be to achieve that level of certainty.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        
        self.variable_4_info_label = QLabel("<b>σ</b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("The true variance of the underlying population." \
                                        "It measures the spread of the data.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.variable_5_info_label = QLabel("<b>n</b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("The true standard deviation of the entire population."
                                        "It measures the amount of variation or dispersion in the data."
                                        "A higher σ means the data is more spread out, which results in a wider, less precise confidence interval.")
        self.variable_5_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_5_info,4,1)

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
        self.variable_1_display = "<i>X̄</i>"
        self.variable_2_display = "n"
        self.variable_3_display = "<i>&sigma;</i>"
        self.variable_4_display = "Z"


        self.raw_text = self.variable_1_input.toPlainText().strip()
        self.variable_3_raw = self.variable_2_input.text().strip()
        self.variable_4_raw = self.variable_3_input.text().strip()

        if not self.raw_text:
            self.variable_1 = None
            self.variable_2 = None
        else:
            try:
                data = [float(x.strip()) for x in self.raw_text.split(",") if x.strip()]
                self.variable_2 = len(data)
                self.variable_1 = sum(data) / len(data)
                self.variable_1_display = f"{self.variable_1:.2f}"
                self.variable_2_display = f"{self.variable_2}"
            except Exception as e:
                self.current_result = "<span style='color: #EF4444;'>No Data!</span>"

        if not self.variable_3_raw:
            self.variable_3 = None
        else:
            self.variable_3_display = float(self.variable_3_raw)

        if not self.variable_4_raw:
            self.variable_4 = None
        else:
            self.variable_4 = float(self.variable_4_raw)
            if self.variable_4 < 0 or self.variable_4 > 100:
                self.current_result = "<span style='color: #EF4444;'>Invalid CL Input!</span>"
            else:
                try:
                    alpha = 1 - (self.variable_4 / 100)
                    area = 1 - (alpha / 2)
                    self.variable_4 = statistics.NormalDist().inv_cdf(area)
                    self.variable_4_display = f"{self.variable_4:.2f}"
                except statistics.StatisticsError:
                    self.current_result = "<span style='color: #EF4444;'>Invalid CL Input!</span>"
            


        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        {self.variable_1_display} &plusmn; 
                    </td>
                    
                    <td valign="middle" style="padding-right: 10px;">
                        {self.variable_4_display}<sup>*</sup>
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                    {self.variable_3_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 5px 10px;">
                                    &radic;{self.variable_2_display}
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
            self.variable_3 = float(self.variable_3_display)
            self.variable_4 = float(self.variable_4_display)
            margin_of_error = self.variable_4 * (self.variable_3 / math.sqrt(self.variable_2))
            base = self.variable_1 - margin_of_error
            top = self.variable_1 + margin_of_error
            result = f"[{base:.2f}, \t {top:.2f}]"

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>Invalid &sigma; or CL Input!</span>"
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

        