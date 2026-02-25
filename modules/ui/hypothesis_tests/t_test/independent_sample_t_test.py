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

        self.regex = QRegularExpressionValidator(QRegularExpression("[0-9. ]+"))

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("Data 1")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0,1,2)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0,1,2)

        self.variable_2_label = QLabel("Data 2")
        self.variable_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_2_label,2,0,1,2)

        self.variable_2_input = QTextEdit()
        self.variable_2_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_2_input,3,0,1,2)

        self.variable_3_label = QLabel("<i>&alpha;</i>")
        self.left_group_box_layout.addWidget(self.variable_3_label,4,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("Significance Level")
        self.left_group_box_layout.addWidget(self.variable_3_input,4,1)

        self.variable_4_label = QLabel("Test")
        self.left_group_box_layout.addWidget(self.variable_4_label,5,0)

        self.variable_4_input = QComboBox()
        self.variable_4_input.addItems(["One-Tailed (Right)","One-Tailed (Left)","Two-Tailed"])
        self.left_group_box_layout.addWidget(self.variable_4_input,5,1)

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

        self.variable_1_info = QTextEdit("<b>Independent T-Test:</b><br>"
                                        "Compares the means of two unrelated groups to determine if they are significantly different from each other.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("<i>X̄</i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b><i>X̄</i> (Sample Mean):</b><br>"
                                        "The average value of a specific sample. Represents the center of your data group.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("<b><i>s</i><sup>2</sup></b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b><i>s</i><sup>2</sup> (Sample Variance):</b><br>"
                                        "Measures how spread out the data points are from the mean. It is the square of the standard deviation.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        
        self.variable_4_info_label = QLabel("<b><i>n</i></b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b><i>n</i> (Sample Size):</b><br>"
                                        "The total number of observations or data points in a given sample group.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)


        self.variable_5_info_label = QLabel("<b>df</b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("<b>df (Degrees of Freedom):</b><br>"
                                        "Determines the shape of the t-distribution. Calculated using Welch's approximation for unequal variances.")
        self.variable_5_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_5_info,4,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.textChanged.connect(self.reset_and_update_display)
        self.variable_4_input.currentTextChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = "<i>X̄<sub>1</sub></i>"
        self.variable_2_display = "<i>n<sub>1</sub></i>"
        self.variable_3_display = "<i>s<sub>1</sub><sup>2</sup></i>"

        self.variable_4_display = "<i>X̄<sub>2</sub></i>"
        self.variable_5_display = "<i>n<sub>2</sub></i>"
        self.variable_6_display = "<i>s<sub>2</sub><sup>2</sup></i>"

        self.variable_7_display = self.variable_3_input.text().strip()
        self.variable_8 = self.variable_4_input.currentText()

        self.variable_1_2_3_raw = self.variable_1_input.toPlainText().strip()
        self.variable_4_5_6_raw = self.variable_2_input.toPlainText().strip()

        if not self.variable_1_2_3_raw:
            self.variable_1 = None
            self.variable_2 = None
            self.variable_3 = None
        else:
            try:
                data = [float(x.strip()) for x in self.variable_1_2_3_raw.split(",") if x.strip()]
                self.variable_2 = len(data)
                self.variable_1 = sum(data) / self.variable_2
                self.variable_3 = statistics.stdev(data) ** 2
                self.variable_1_display = f"{self.variable_1:.2f}"
                self.variable_2_display = f"{self.variable_2}"
                self.variable_3_display = f"{self.variable_3:.2f}"
            except :
                    self.current_result = "<span style='color: #EF4444;'>Data 1 Invalid Input!</span>"
                    self.variable_1_display = "<i>X̄<sub>1</sub></i>"
                    self.variable_2_display = "<i>n<sub>1</sub></i>"
                    self.variable_3_display = "<i>s<sub>1</sub><sup>2</sup></i>"

        if not self.variable_4_5_6_raw:
            self.variable_4 = None
            self.variable_5 = None
            self.variable_6 = None
        else:
            try:
                data = [float(x.strip()) for x in self.variable_4_5_6_raw.split(",") if x.strip()]
                self.variable_5 = len(data)
                self.variable_4 = sum(data) / self.variable_5
                self.variable_6 = statistics.stdev(data) ** 2
                self.variable_4_display = f"{self.variable_4:.2f}"
                self.variable_5_display = f"{self.variable_5}"
                self.variable_6_display = f"{self.variable_6:.2f}"
            except :
                    self.current_result = "<span style='color: #EF4444;'>Data 2 Invalid Input!</span>"
                    self.variable_4_display = "<i>X̄<sub>2</sub></i>"
                    self.variable_5_display = "<i>n<sub>2</sub></i>"
                    self.variable_6_display = "<i>s<sub>2</sub><sup>2</sup></i>"

        if not self.variable_7_display:
            self.variable_7 = None
        else:
            try:
                self.variable_7 = float(self.variable_7_display)
                if self.variable_7 <= 0:
                    self.current_result = "<span style='color: #EF4444;'>&alpha; &gt; 0!</span>"
                elif self.variable_7 >= 1:
                    self.variable_7 = self.variable_7 / 100
            except:
                self.current_result = "<span style='color: #EF4444;'> 0 &gt; &alpha; &lt; 1 !</span>"
    
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px; font-style: italic;">
                        t = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 6px 10px;">
                                    {self.variable_1_display} &minus; {self.variable_4_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 8px 10px 0 10px;">
                                    
                                    <table cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td valign="center" style="font-size: 80px;line-height: 0.8;">
                                                &radic;
                                            </td>
                                            <td valign="middle" style="border-top: 2px solid #ADBAC7; padding-top: 6px; width: 200px;">
                                                
                                                <table cellpadding="0" cellspacing="0" align="center">
                                                    <tr>
                                                        <td align="center">
                                                            <table cellpadding="0" cellspacing="0">
                                                                <tr><td align="center" style="border-bottom: 1px solid currentColor; padding: 0 6px 2px 6px; font-size: 30px;">{self.variable_3_display}</td></tr>
                                                                <tr><td align="center" style="padding: 2px 6px 0 6px; font-size: 30px;">{self.variable_2_display}</td></tr>
                                                            </table>
                                                        </td>
                                                        
                                                        <td valign="middle" style="padding: 0 10px;">
                                                        +
                                                        </td>
                                                        
                                                        <td align="center">
                                                            <table cellpadding="0" cellspacing="0">
                                                                <tr><td align="center" style="border-bottom: 1px solid currentColor; padding: 0 6px 2px 6px; font-size: 30px;">{self.variable_6_display}</td></tr>
                                                                <tr><td align="center" style="padding: 2px 6px 0 6px; font-size: 30px;">{self.variable_5_display}</td></tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>

                                            </td>
                                        </tr>
                                    </table>

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
            t_score = (self.variable_1 - self.variable_4) / (math.sqrt((self.variable_3 / self.variable_2)+(self.variable_6 / self.variable_5)))

            v1 = self.variable_3 / self.variable_2
            v2 = self.variable_6 / self.variable_5
            df = ((v1 + v2) ** 2) / (((v1 ** 2) / (self.variable_2 - 1)) + ((v2 ** 2) / (self.variable_5 - 1)))

            if self.variable_8 == "Two-Tailed":
                p_value = 2 * (1 - stats.t.cdf(abs(t_score),df=df))
            
            elif self.variable_8 == "One-Tailed (Right)":
                p_value = 1 - stats.t.cdf(t_score,df=df)

            else:
                p_value = stats.t.cdf(t_score,df=df)

            if p_value < self.variable_7:
                decision = "Reject H₀"
                decision_color = "#10B981"
            else:
                decision = "Fail to Reject H₀"
                decision_color = "#F59E0B"   

            result_html = f"""
                    <span style='color: #3B82F6; font-weight: bold;'>{t_score:.3f}</span>
                    <span style='font-size: 20px; color: gray;'><i>p-value: {p_value:.4f}</i></span>
                    <span style='font-size: 16px; color: gray;'><i>df: {df:.2f}</i></span>
                    <span style='font-size: 25px; color: {decision_color}; font-weight: bold;'>{decision}</span>
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
