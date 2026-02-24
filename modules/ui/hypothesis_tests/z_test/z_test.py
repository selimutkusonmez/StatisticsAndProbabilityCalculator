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

        self.variable_1_label = QLabel("Sample Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0,1,2)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0,1,2)

        self.variable_2_label = QLabel("<i>&mu;<sub>0</sub></i>")
        self.left_group_box_layout.addWidget(self.variable_2_label,2,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(QRegularExpressionValidator(QRegularExpression("[-0-9. ]+")))
        self.variable_2_input.setPlaceholderText("Hypothesized Mean")
        self.left_group_box_layout.addWidget(self.variable_2_input,2,1)

        self.variable_3_label = QLabel("<i>&sigma;</i>")
        self.left_group_box_layout.addWidget(self.variable_3_label,3,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("Population STD")
        self.left_group_box_layout.addWidget(self.variable_3_input,3,1)

        self.variable_4_label = QLabel("<i>&alpha;</i>")
        self.left_group_box_layout.addWidget(self.variable_4_label,4,0)

        self.variable_4_input = QLineEdit()
        self.variable_4_input.setValidator(self.regex)
        self.variable_4_input.setPlaceholderText("Significance Level")
        self.left_group_box_layout.addWidget(self.variable_4_input,4,1)

        self.variable_5_label = QLabel("Test")
        self.left_group_box_layout.addWidget(self.variable_5_label,5,0)

        self.variable_5_input = QComboBox()
        self.variable_5_input.addItems(["One-Tailed (Right)","One-Tailed (Left)","Two-Tailed"])
        self.left_group_box_layout.addWidget(self.variable_5_input,5,1)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,6,0,1,2)

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

        self.variable_1_info = QTextEdit("<b>Z-Test:</b><br>A statistical hypothesis test used to determine whether a sample mean significantly differs from a known population mean" \
        "                                It requires a known population standard deviation (&sigma;) and typically a large sample size (n &ge; 30).")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("<i>X̄</i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b><i>X̄</i> (Sample Mean):</b>"
                                        "The average calculated from your sample data. It is the observed value that you are testing against the hypothesized population mean.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("<b>&mu;<sub>0</sub></b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>&mu;<sub>0</sub> (Hypothesized Mean):</b><br>"
                                        "The assumed mean of the population under the null hypothesis (H₀). It serves as the baseline, historical, or expected target value for your test.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        
        self.variable_4_info_label = QLabel("<b>&sigma;</b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b>&sigma; (Population STD):</b><br>The known standard deviation of the entire population."
                                        "It measures the true variability or spread of the data. If this is unknown, a T-Test should be used instead.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.variable_5_info_label = QLabel("<b>&alpha;</b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("<b>&alpha; (Significance Level):</b><br>The threshold for statistical significance (commonly 0.05)." \
                                        "It represents the maximum acceptable risk of rejecting the null hypothesis when it is actually true (Type I error rate).")
        self.variable_5_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_5_info,4,1)

        self.variable_6_info_label = QLabel("<b>n</b>")
        self.right_group_box_layout.addWidget(self.variable_6_info_label,5,0)

        self.variable_6_info = QTextEdit("<b>n (Sample Size):</b><br>The total number of data points in your sample."
                                        "Larger sample sizes reduce the standard error, making the test more precise and reliable.")
        self.variable_6_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_6_info,5,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.textChanged.connect(self.reset_and_update_display)
        self.variable_4_input.textChanged.connect(self.reset_and_update_display)
        self.variable_5_input.currentTextChanged.connect(self.reset_and_update_display)


    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = "<i>X̄</i>"
        self.variable_2_display = "n"
        self.variable_3_display = "<i>&mu;<sub>0</sub></i>"
        self.variable_4_display = "<i>&sigma;</i>"
        self.variable_5_display = "<i>&alpha;</i>"

        self.raw_text = self.variable_1_input.toPlainText().strip()
        self.variable_3_raw = self.variable_2_input.text().strip()
        self.variable_4_raw = self.variable_3_input.text().strip()
        self.variable_5_raw = self.variable_4_input.text().strip()
        self.variable_6 = self.variable_5_input.currentText()

        if not self.raw_text:
            self.variable_1 = None
            self.variable_2 = None
        else:
            try:
                data = [float(x.strip()) for x in self.raw_text.split(",") if x.strip()]
                self.variable_2 = len(data)
                self.variable_1 = sum(data) / len(data)
                self.variable_1_display = f"{self.variable_1:.2f}"
                self.variable_2_display = f"{self.variable_2:.2f}"
            except ValueError:
                    self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
                    self.variable_1 = "<i>X̄</i>"
                    self.variable_2 = "n"

        if not self.variable_3_raw:
            self.variable_3 = None
        else:
            try:
                self.variable_3 = float(self.variable_3_raw)
                self.variable_3_display = f"{self.variable_3:.2f}"
            except:
                pass

            
        if not self.variable_4_raw:
            self.variable_4 = None
        else:
            try:
                self.variable_4 = float(self.variable_4_raw)
                self.variable_4_display = f"{self.variable_4:.2f}"
            except:
                pass

            
        if not self.variable_5_raw:
            self.variable_5 = None
        else:
            try:
                self.variable_5 = float(self.variable_5_raw)
                if self.variable_5 <= 0:
                    self.current_result = "<span style='color: #EF4444;'>&alpha; &gt; 0!</span>"
                elif self.variable_5 >= 1:
                    self.variable_5 = self.variable_5 / 100
                
                self.variable_5_display = f"{self.variable_5:.2f}"
            except:
                pass

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        Z = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                    {self.variable_1_display} &minus; {self.variable_3_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 0 10px;">
                                    {self.variable_4_display} / &radic;{self.variable_2_display}
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
            z_score = (self.variable_1 - self.variable_3) / (self.variable_4 / math.sqrt(self.variable_2))

            dist = statistics.NormalDist()

            if self.variable_6 == "Two-Tailed":
                p_value = 2 * (1 - dist.cdf(abs(z_score)))
            
            elif self.variable_6 == "One-Tailed (Right)":
                p_value = 1 - dist.cdf(z_score)

            else:
                p_value = dist.cdf(z_score)

            if p_value < self.variable_5:
                decision = "Reject H₀"
                decision_color = "#10B981"
            else:
                decision = "Fail to Reject H₀"
                decision_color = "#F59E0B"   

            result_html = f"""
                <div style="text-align: left; padding-left: 10px;">
                    <span style='color: #3B82F6; font-weight: bold;'>{z_score:.3f}</span><br>
                    <span style='font-size: 20px; color: gray;'><i>p-value: {p_value:.4f}</i></span><br>
                    <span style='font-size: 25px; color: {decision_color}; font-weight: bold;'>{decision}</span>
                </div>
            """

            self.current_result = result_html

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>Invalid X Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444;'>Div by Zero!</span>"
        except TypeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
        except Exception:
            self.current_result = "<span style='color: #EF4444;'>Error!</span>"

        self.update_formula_display()



        