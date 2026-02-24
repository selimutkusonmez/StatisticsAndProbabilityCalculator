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

        self.variable_1_label = QLabel("Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0,1,2)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,4]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0,1,2)

        self.variable_2_label = QLabel("x")
        self.left_group_box_layout.addWidget(self.variable_2_label,2,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Target Value")
        self.left_group_box_layout.addWidget(self.variable_2_input,2,1)

        self.variable_3_label = QLabel("Dataset Type")
        self.left_group_box_layout.addWidget(self.variable_3_label,3,0)

        self.variable_3_input = QComboBox()
        self.variable_3_input.addItems(["Population","Sample"])
        self.left_group_box_layout.addWidget(self.variable_3_input,3,1)

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

        self.variable_1_info = QTextEdit("<b>Log-Normal Distribution:</b><br>"
                                        "A continuous probability distribution of a random variable whose <b>logarithm is normally distributed</b>. "
                                        "Unlike the normal distribution, it is skewed to the right and only exists for <b>positive values (x > 0)</b>.<br><br>"
                                        "<i>Commonly used for values that cannot be negative, such as stock prices, income, or rainfall amounts.</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("<i>&mu;</i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b>&mu; (Mu / Mean):</b><br>"
                                        "The central or typical value of the distribution. It dictates where the peak of the bell curve is located. "
                                        "It can be any real number")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("<i>&sigma;</i>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>&sigma; (Sigma / Standard Deviation):</b><br>"
                                        "A measure of the amount of variation or dispersion. It determines how 'fat' or 'skinny' the bell curve is. "
                                        "This must be strictly greater than 0 (<b>&sigma; > 0</b>).")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        
        self.variable_4_info_label = QLabel("x")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b>x (Target Value):</b><br>"
                                        "The specific value on the continuous scale that you are evaluating.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)
        self.variable_3_input.currentTextChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_3 = self.variable_3_input.currentText()
        self.variable_4_display =  self.variable_2_input.text().strip() or "x"
        if self.variable_3 == "Population":
            self.variable_2_display = "<i>&sigma;</i>"
            self.variable_1_display = "<i>&mu;</i>"
        else:
            self.variable_2_display = "s"
            self.variable_1_display = "<i>x&#772;</i>"
        
        raw_text = self.variable_1_input.toPlainText().strip()
        if not raw_text:
            self.variable_1 = None
            self.variable_2 = None
        else : 
            try:
                data = [float(x.strip()) for x in raw_text.split(",") if x.strip()]
                data = [math.log(d) for d in data if d > 0]
                if not data:
                    raise ZeroDivisionError
                self.variable_1 = sum(data) / len(data)
                self.variable_1_display = f"{self.variable_1:.2f}"
                if self.variable_3 == "Population":
                    self.variable_2 = statistics.pstdev(data)
                else:
                    self.variable_2 = statistics.stdev(data)
                self.variable_2_display = f"{self.variable_2:.2f}"  
                       
            except ValueError:
                self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
                self.variable_1 = "<i>&mu;</i>"
            except :
                self.current_result = "<span style='color: #EF4444;'>All Values Must be > 0</span>"
                self.variable_1 = "<i>&mu;</i>"

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 22px;">
                        <i>f({self.variable_4_display})</i> = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0" style="font-size: 36px;">
                            <tr>
                                <td align="center" style="border-bottom: 3px solid currentColor; padding: 0px 12px 6px 12px;">
                                    1
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 6px 12px 0px 12px;">
                                    {self.variable_4_display}&times;{self.variable_2_display}&radic;<span style="text-decoration: overline;">2&pi;</span>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 15px; font-size: 51px;">
                        <i>e</i>
                    </td>

                    <td valign="top" style="padding-top: 8px;"> <table cellpadding="0" cellspacing="0" style="font-size: 27px;">
                            <tr>
                                <td rowspan="2" valign="middle" style="padding-right: 8px; font-size: 33px;">
                                    &minus;
                                </td>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 6px 3px 6px;">
                                    (ln{self.variable_4_display} &minus; {self.variable_1_display})<sup>2</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 3px 6px 0px 6px;">
                                    2&times;{self.variable_2_display}<sup>2</sup>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 30px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            self.variable_4= float(self.variable_4_display)
            if self.variable_4 <= 0:result = 0
            else:
                result = (1 / (self.variable_4 * self.variable_2 * math.sqrt(2 * math.pi))) * (math.e ** (-((math.log(self.variable_4) - self.variable_1)**2) / (2 * (self.variable_2 ** 2))))

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>No X Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444;'>Data length &gt; 1!</span>"
        except TypeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
        except Exception:
             self.current_result = "<span style='color: #EF4444;'>Error!</span>"

        self.update_formula_display()



        