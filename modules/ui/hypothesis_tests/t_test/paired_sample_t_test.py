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

        self.variable_1_info = QTextEdit("<b>Paired T-Test:</b><br>"
                                        "Compares the means of two related groups (e.g., before and after measurements on the same subjects) to detect significant differences.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("<b><i>d̄</i></b>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b><i>d̄</i> (Mean Difference):</b><br>"
                                        "The average of the differences between each pair of observations.")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("<b><i>s<sub>d</sub></i></b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b><i>s<sub>d</sub></i> (Std Dev of Differences):</b><br>"
                                        "Measures the spread or variability of the paired differences.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)
        
        self.variable_4_info_label = QLabel("<b><i>n</i></b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b><i>n</i> (Number of Pairs):</b><br>"
                                        "The total number of paired observations. Both data sets must have exactly the same length.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.variable_5_info_label = QLabel("<b>df</b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("<b>df (Degrees of Freedom):</b><br>"
                                        "Calculated simply as n - 1 for a paired test.")
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
        self.variable_5_display = "<i>d&#772;</i>"
        self.variable_2_display = "n"
        self.variable_6_display = "<i>s<sub>d</sub></i>"

        self.variable_1_raw = self.variable_1_input.toPlainText().strip()
        self.variable_2_raw = self.variable_2_input.toPlainText().strip()

        self.variable_8_raw = self.variable_3_input.text().strip() #alpha
        self.variable_7 = self.variable_4_input.currentText() #type
        
        if not self.variable_1_raw:
            self.variable_1 = None
            self.variable_2 = None
        else:
            try:
                self.variable_1 = [float(x.strip()) for x in self.variable_1_raw.split(",") if x.strip()]
                self.variable_2 = len(self.variable_1)
                if self.variable_2 == 1:
                    self.current_result = "<span style='color: #EF4444;'>Data length &gt; 1!</span>"
            except ValueError:
                self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"

        if not self.variable_2_raw:
            self.variable_1 = None
            self.variable_2 = None
            self.variable_3 = None
            self.variable_4 = None
        else:
            try:
                self.variable_3 = [float(x.strip()) for x in self.variable_2_raw.split(",") if x.strip()]
                self.variable_4 = len(self.variable_3)
                if self.variable_1 is not None and self.variable_3 is not None:
                    if self.variable_2 == self.variable_4:
                        differences = [self.variable_1[i] - self.variable_3[i] for i in range(self.variable_2)]
                        self.variable_5 = sum(differences) / self.variable_2
                        self.variable_6 = statistics.stdev(differences)
                        self.variable_5_display = f"{self.variable_5:.2f}"
                        self.variable_6_display = f"{self.variable_6:.2f}"
                        self.variable_2_display = f"{self.variable_2}"
                    else:
                        self.current_result = "<span style='color: #EF4444;'>Invalid Data Length!</span>"
            except ValueError:
                self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
            except statistics.StatisticsError:
                self.current_result = "<span style='color: #EF4444;'>Data Length &gt; 1</span>"

        if not self.variable_8_raw:
            self.variable_8 = None
        else:
            try:
                self.variable_8 = float(self.variable_8_raw)
                if self.variable_8 <= 0:
                    self.current_result = "<span style='color: #EF4444;'>&alpha; &gt; 0!</span>"
                elif self.variable_8 >= 1:
                    self.variable_8 = self.variable_8 / 100
            except:
                self.current_result = "<span style='color: #EF4444;'> 0 &gt; &alpha; &lt; 1 !</span>"
    
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        t = 
                    </td>
                    
                    <td align="center">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid; padding: 0 10px 6px 10px;">
                                    {self.variable_5_display}
                                </td>
                            </tr>
                            
                            <tr>
                                <td align="center" >
                                    <table cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td align="center" padding: 2px 8px 6px 8px;">
                                                {self.variable_6_display}&times;&radic;{self.variable_2_display}
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
            if self.variable_6 == 0:
                raise ZeroDivisionError
            
            t_score = self.variable_5 / (self.variable_6 / math.sqrt(self.variable_2))

            df = self.variable_2 - 1

            if self.variable_7 == "Two-Tailed":
                p_value = 2 * (1 - stats.t.cdf(abs(t_score), df=df))
            
            elif self.variable_7 == "One-Tailed (Right)":
                p_value = 1 - stats.t.cdf(t_score, df=df)

            else:
                p_value = stats.t.cdf(t_score, df=df)

            if p_value < self.variable_8:
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
