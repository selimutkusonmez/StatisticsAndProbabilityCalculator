from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QTextEdit,QVBoxLayout,QHBoxLayout


class OperationWidget(QWidget):
    def __init__(self,operation_name):
        super().__init__()
        self.operation_name = operation_name
        self.init_ui()

    def init_ui(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.current_result = "<i>Waiting...</i>"

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(250)

        self.variable_1_label = QLabel("Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma : [1,2,3,0.2,-1]")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_button_function)
        self.left_group_box_layout.addWidget(self.calculate_button,2,0,1,2)

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

        self.variable_1_info_label = QLabel("&sigma;<sup>2</sup>")
        self.right_group_box_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>&sigma;<sup>2</sup> (Population Variance):</b><br>"
                                        "It measures the average squared distance of each data point from the population mean."
                                        "It quantifies the spread or dispersion within the entire dataset.")
        self.variable_1_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("<i><b>&mu;</b></i>")
        self.right_group_box_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>&mu; (Population Mean):</b> The average value of all observations in the entire population.<br><br>")
        self.variable_2_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("N")
        self.right_group_box_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>N (Population Size):</b> The total number of members or data points in the population.")
        self.variable_3_info.setReadOnly(True)
        self.right_group_box_layout.addWidget(self.variable_3_info,2,1)

        self.update_formula_display()
        self.left_hide = False
        self.right_hide = False

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)


    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()


    def update_formula_display(self):
            
        raw_text = self.variable_1_input.toPlainText().strip()
        if not raw_text:
                self.variable_1_display = "&mu;"
                self.variable_2_display = "N"
                self.variable_1 = None
                self.variable_2 = None
                self.data = None
        else : 
            try:
                self.data = [float(x.strip()) for x in raw_text.split(",") if x.strip()]
                self.variable_2 = len(self.data)
                self.variable_1 = sum(self.data) / self.variable_2
                self.variable_1_display = f"{self.variable_1:.2f}"
                self.variable_2_display = f"{self.variable_2:.2f}"
                
            except ValueError:
                self.current_result = "<span style='color: #EF4444;'>Invalid Input!</span>"
                self.variable_1_display = "&mu;"
                self.variable_2_display = "N"
    
            
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        <i>&sigma;<sup>2</sup></i> = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 8px;">
                                    &Sigma;(x<sub>i</sub> - {self.variable_1_display})<sup>2</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 8px 0px 8px;">
                                    {self.variable_2_display}
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 10px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
            """
        self.dynamic_formula.setText(html_formul)

    def calculate_button_function(self):
        try:
            result = sum((x - self.variable_1) ** 2 for x in self.data)/self.variable_2

            self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except TypeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"

        except AttributeError:
            self.current_result = "<span style='color: #EF4444;'>No Data!</span>"
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

        