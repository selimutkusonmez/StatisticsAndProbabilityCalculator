from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QTextEdit,QVBoxLayout,QHBoxLayout
from PyQt6.QtGui import QRegularExpressionValidator

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

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,6,0,1,2)

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

        self.right_group_box.setFixedWidth(375)

        self.variable_1_info_label = QLabel()
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>Chi-Square Goodness of Fit:</b><br>"
                                        "Determines how well observed data fits an expected distribution. It uses frequency counts, not means or variances.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("<b><i>O</i></b>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b><i>O</i> (Observed Frequencies):</b><br>"
                                        "The actual counts or frequencies observed in your sample data (Data 1).")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("<b><i>E</i></b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b><i>E</i> (Expected Frequencies):</b><br>"
                                        "The theoretical counts expected if the null hypothesis is true (Data 2). Expected values should ideally be &ge; 5.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)
        
        self.variable_4_info_label = QLabel("<b><i>k</i></b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b><i>k</i> (Categories):</b><br>"
                                        "The total number of distinct categories or groups being compared. Both data sets must have <i>k</i> items.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.variable_5_info_label = QLabel("<b>df</b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("<b>df (Degrees of Freedom):</b><br>"
                                        "Calculated as k - 1. It defines the shape of the Chi-Square distribution curve.")
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
        self.variable_1_raw = self.variable_1_input.toPlainText().strip()
        self.variable_3_raw = self.variable_2_input.toPlainText().strip()
        self.variable_5_raw = self.variable_3_input.text().strip()

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

        if not self.variable_3_raw:
            self.variable_3 = None
            self.variable_4 = None
        else:
            try:
                self.variable_3 = [float(x.strip()) for x in self.variable_3_raw.split(",") if x.strip()]
                self.variable_4 = len(self.variable_3)
                if self.variable_1 is not None and self.variable_3 is not None:
                    if self.variable_2 == self.variable_4:
                        self.chi_sq = 0
                        for o, e in zip(self.variable_1, self.variable_3):
                            if e == 0:
                                raise ZeroDivisionError
                            self.chi_sq += ((o - e) ** 2) / e
                    else:
                        self.current_result = "<span style='color: #EF4444;'>Invalid Data Length!</span>"
            except ValueError:
                self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
            except ZeroDivisionError:
                self.current_result = "<span style='color: #EF4444;'>Expected value cannot be 0!</span>"

        if not self.variable_5_raw:
            self.variable_5 = None
        else:
            try:
                self.variable_5 = float(self.variable_5_raw)
                if self.variable_5 <= 0:
                    self.current_result = "<span style='color: #EF4444;'>&alpha; &gt; 0!</span>"
                elif self.variable_5 >= 1:
                    self.variable_5 = self.variable_5 / 100
            except:
                self.current_result = "<span style='color: #EF4444;'> 0 &gt; &alpha; &lt; 1 !</span>"
    

        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px; font-size: 32px; font-style: italic;">
                        &chi;<sup>2</sup> = &Sigma;
                    </td>
                    <td align="center">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px; font-size: 26px;">
                                    (O &minus; E)<sup>2</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 6px 10px 0 10px; font-size: 26px;">
                                    E
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td valign="middle" style="padding-left: 20px; font-size: 30px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)


    def calculate_button_function(self):
        try:   
            df = self.variable_2 - 1         
            p_value = 1 - stats.chi2.cdf(self.chi_sq, df=df)

            if p_value < self.variable_5:
                decision = "Reject H₀"
                decision_color = "#10B981"
            else:
                decision = "Fail to Reject H₀"
                decision_color = "#F59E0B"   

            result_html = f"""
                    <span style='color: #3B82F6; font-size: 30px; font-weight: bold;'>{self.chi_sq:.3f}</span>
                    <span style='font-size: 20px; color: gray;'><i>p-value: {p_value:.4f}</i></span>
                    <span style='font-size: 16px; color: gray;'><i>df: {df}</i></span>
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
