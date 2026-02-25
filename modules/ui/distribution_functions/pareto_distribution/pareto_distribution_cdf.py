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

        self.variable_1_label = QLabel("<i>&alpha;</i>")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QLineEdit()
        self.variable_1_input.setValidator(self.regex)
        self.variable_1_input.setPlaceholderText("Shape Parameter (\u03b1 > 0)")
        self.left_group_box_layout.addWidget(self.variable_1_input,0,1)

        self.variable_2_label = QLabel("x<sub>m</sub>")
        self.left_group_box_layout.addWidget(self.variable_2_label,2,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Minimum Value (xm > 0)")
        self.left_group_box_layout.addWidget(self.variable_2_input,2,1)

        self.variable_3_label = QLabel("x")
        self.left_group_box_layout.addWidget(self.variable_3_label,3,0)

        self.variable_3_input = QLineEdit()
        self.variable_3_input.setValidator(self.regex)
        self.variable_3_input.setPlaceholderText("Target Value (x \u2265 xm)")
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

        self.variable_1_info = QTextEdit("<b>Pareto Distribution:</b><br>"
                                        "A power-law probability distribution that is used to describe social, scientific, and geophysical phenomena. "
                                        "It is most famous for the <b>80/20 rule</b> (e.g., 80% of wealth is owned by 20% of the population).<br><br>"
                                        "<i>Unlike the normal distribution, it is highly skewed and 'heavy-tailed', meaning extreme values are more likely than expected.</i>")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("<i>&alpha;</i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b>&alpha; (Alpha / Shape Parameter):</b><br>"
                                        "Also known as the Pareto index. It determines how fast the tail of the distribution decays. "
                                        "A smaller &alpha; leads to a 'heavier' tail (more extreme values). Must be strictly greater than 0 (<b>&alpha; > 0</b>).")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("<i>x<sub>m</sub></i>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>x<sub>m</sub> (Scale Parameter / Minimum):</b><br>"
                                        "The minimum possible value for the random variable. The distribution only exists for values starting from this point. "
                                        "This must be strictly greater than 0 (<b>x<sub>m</sub> > 0</b>).")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        
        self.variable_4_info_label = QLabel("x")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b>x (Target Value):</b><br>"
                                        "The specific value you are evaluating. For Pareto distributions, <b>x must be greater than or equal to x<sub>m</sub></b>.<br><br>"
                                        "<i>If x &lt; x<sub>m</sub>, the probability density is exactly 0.</i>")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

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
        self.variable_1_display = "&alpha;"
        self.variable_2_display = "x<sub>m</sub>"
        self.variable_3_display = "x"

        self.variable_1_raw = self.variable_1_input.text().strip()
        self.variable_2_raw = self.variable_2_input.text().strip()
        self.variable_3_raw = self.variable_3_input.text().strip()

        self.variable_1 = None
        self.variable_2 = None
        self.variable_3 = None
        
        if self.variable_1_raw:
            try:
                val = float(self.variable_1_raw)
                if val > 0:
                    self.variable_1 = val
                    self.variable_1_display = f"{self.variable_1:.2f}"
            except ValueError:
                pass

        if self.variable_2_raw:
            try:
                val = float(self.variable_2_raw)
                if val > 0:
                    self.variable_2 = val
                    self.variable_2_display = f"{self.variable_2:.2f}"
            except ValueError:
                pass

        if self.variable_3_raw:
            try:
                self.variable_3 = float(self.variable_3_raw)
                self.variable_3_display = f"{self.variable_3:.2f}"
            except ValueError:
                pass
        
        if not self.variable_1_raw:
            self.current_result = "<span style='color: #EF4444;'>&alpha; is None!</span>"
        elif self.variable_1 is None:
            self.current_result = "<span style='color: #EF4444;'>&alpha; &gt; 0!</span>"

        elif not self.variable_2_raw:
            self.current_result = "<span style='color: #EF4444;'>x<sub>m</sub> is None!</span>"
        elif self.variable_2 is None:
            self.current_result = "<span style='color: #EF4444;'>x<sub>m</sub> &gt; 0!</span>"

        elif not self.variable_3_raw:
            self.current_result = "<span style='color: #EF4444;'>x is None!</span>"
        elif self.variable_3 is None:
            self.current_result = "<span style='color: #EF4444;'>Invalid x!</span>"

        elif self.variable_3 < self.variable_2:
            self.current_result = "<span style='color: #EF4444;'>x &ge; x<sub>m</sub>!</span>"


        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle">
                        <i>F({self.variable_3_display})</i> = 1 &minus; 
                    </td>
                    
                    <td valign="middle" style="font-size: 50px; font-weight: 300; padding-bottom: 5px;">
                        (
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor;">
                                    <i>{self.variable_2_display}</i>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" >
                                    <i>{self.variable_3_display}</i>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="font-size: 50px; font-weight: 300; padding-bottom: 5px;">
                        )
                    </td>
                    
                    <td valign="top" >
                        {self.variable_1_display}
                    </td>

                    <td valign="middle" >
                        , <i>{self.variable_3_display}</i> &ge; <i>{self.variable_2_display}</i>
                    </td>

                    <td valign="middle" >
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            result = 1 - ((self.variable_2 / self.variable_3) ** self.variable_1)

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except ValueError:
            self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
        except ZeroDivisionError:
            self.current_result = "<span style='color: #EF4444;'>Div by Zero!</span>"
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

        