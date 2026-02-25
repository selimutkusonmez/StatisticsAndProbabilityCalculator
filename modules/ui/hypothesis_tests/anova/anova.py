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

        self.variable_1_label = QLabel("Groups Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0,1,2)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0,1,2)

        self.variable_2_label = QLabel("<i>&alpha;</i>")
        self.left_group_box_layout.addWidget(self.variable_2_label,4,0)

        self.variable_2_input = QLineEdit()
        self.variable_2_input.setValidator(self.regex)
        self.variable_2_input.setPlaceholderText("Significance Level")
        self.left_group_box_layout.addWidget(self.variable_2_input,4,1)

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

        self.variable_1_info = QTextEdit("<b>One-Way ANOVA:</b><br>"
                                        "Compares the means of three or more independent groups to determine if at least one group mean is significantly different from the others.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)

        self.variable_2_info_label = QLabel("<b><i>F</i></b>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)
        
        self.variable_2_info = QTextEdit("<b><i>F</i>-Statistic:</b><br>"
                                        "The ratio of the variance between the groups to the variance within the groups (MSB / MSW).")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)

        self.variable_3_info_label = QLabel("<b><i>k</i></b>")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b><i>k</i> (Number of Groups):</b><br>"
                                        "The total number of independent categories or groups being compared.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)
        
        self.variable_4_info_label = QLabel("<b><i>N</i></b>")
        self.right_group_box_layout.addWidget(self.variable_4_info_label,3,0)

        self.variable_4_info = QTextEdit("<b><i>N</i> (Total Observations):</b><br>"
                                        "The total number of data points across all groups combined.")
        self.variable_4_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_4_info,3,1)

        self.variable_5_info_label = QLabel("<b>df<sub>1</sub><br> df<sub>2</sub></b>")
        self.right_group_box_layout.addWidget(self.variable_5_info_label,4,0)

        self.variable_5_info = QTextEdit("<b>Degrees of Freedom:</b><br>"
                                        "<b>df<sub>1</sub> (Between):</b> k - 1<br>"
                                        "<b>df<sub>2</sub> (Within):</b> N - k")
        self.variable_5_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_5_info,4,1)

        self.update_formula_display()

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)
        self.variable_2_input.textChanged.connect(self.reset_and_update_display)

    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()

    def update_formula_display(self):
        self.variable_1_display = "Mean Square Between"
        self.variable_2_display = "Mean Square Within"
        
        self.groups_raw = self.variable_1_input.toPlainText().strip()
        self.alpha_raw = self.variable_2_input.text().strip()
        
        if not self.groups_raw:
            self.groups = None
        else:
            try:
                raw_groups = self.groups_raw.split("/")
                self.groups = []
                for g in raw_groups:
                    nums = [float(x.strip()) for x in g.split(",") if x.strip()]
                    if nums:  
                        self.groups.append(nums)

                self.groups_size = len(self.groups) # k
                self.total_observations = sum([len(g) for g in self.groups]) # N

                if self.groups_size < 2 or self.total_observations <= self.groups_size:
                    raise ValueError("Not enough data")
            
                self.df_between = self.groups_size - 1
                self.df_within = self.total_observations - self.groups_size

                grand_total = sum([sum(g) for g in self.groups])
                grand_mean = grand_total / self.total_observations

                ssb = 0
                for g in self.groups:
                    group_mean = sum(g) / len(g)
                    ssb += len(g) * ((group_mean - grand_mean) ** 2)
                
                self.msb = ssb / self.df_between

                ssw = 0
                for g in self.groups:
                    group_mean = sum(g) / len(g)
                    for x in g:
                        ssw += (x - group_mean) ** 2
                
                self.msw = ssw / self.df_within
                
                self.variable_1_display = f"{self.msb:.3f}"
                self.variable_2_display = f"{self.msw:.3f}"

            except ValueError:
                self.current_result = "<span style='color: #EF4444;'>Invalid Data!</span>"
                self.variable_1_display = "Mean Square Between"
                self.variable_2_display = "Mean Square Within"
            except ZeroDivisionError:
                self.current_result = "<span style='color: #EF4444;'>Div by Zero!</span>"
                self.variable_1_display = "Mean Square Between"
                self.variable_2_display = "Mean Square Within"
        
        if not self.alpha_raw:
            self.alpha = None
        else:
            try:
                self.alpha = float(self.alpha_raw)
                if self.alpha <= 0:
                    self.current_result = "<span style='color: #EF4444;'>&alpha; &gt; 0!</span>"
                elif self.alpha >= 1:
                    self.alpha = self.alpha / 100
            except:
                self.current_result = "<span style='color: #EF4444;'> 0 &gt; &alpha; &lt; 1 !</span>"


        html_formul = f"""
                <table align="center" cellpadding="0" cellspacing="0" >
                    <tr>
                        <td valign="middle" style="padding-right: 15px;">
                            F = 
                        </td>
                        <td align="center">
                            <table cellpadding="0" cellspacing="0">
                                <tr>
                                    <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                        {self.variable_1_display}
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding: 6px 10px 0 10px;">
                                        {self.variable_2_display}
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
            if self.msw == 0:
                raise ZeroDivisionError

            f_score = self.msb / self.msw

            p_value = stats.f.sf(f_score, self.df_between, self.df_within)

            if p_value < self.alpha:
                decision = "Reject H₀"
                decision_color = "#10B981"
            else:
                decision = "Fail to Reject H₀"
                decision_color = "#F59E0B"   

            result_html = f"""
                <span style='color: #3B82F6; font-size: 30px; font-weight: bold;'>{f_score:.3f}</span>
                <span style='font-size: 18px; color: gray;'><i>p-value: {p_value:.4f}</i></span>
                <span style='font-size: 16px; color: gray;'><i>df: {self.df_between}, {self.df_within}</i></span>
                <span style='font-size: 22px; color: {decision_color}; font-weight: bold;'>{decision}</span>
            """

            self.current_result = result_html

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
