from PyQt6.QtCore import Qt,QRegularExpression,QSize
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QComboBox,QListWidget,QTextEdit,QVBoxLayout
from PyQt6.QtGui import QIcon,QIntValidator,QDoubleValidator,QRegularExpressionValidator

from config import STYLE_PATH

from modules.logic.style_reader.style_reader import read_style

class OperationWidget(QWidget):
    def __init__(self,operation_name):
        super().__init__()
        self.operation_name = operation_name
        self.init_ui()

    def init_ui(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.current_result = "<i>Waiting...</i>"

        validator = QDoubleValidator()
        validator.setRange(0.0, 9999.0, 4)

        #Left GroupBox
        self.left_group_box = QGroupBox()
        self.left_group_box_layout = QGridLayout()
        self.left_group_box.setLayout(self.left_group_box_layout)
        self.layout.addWidget(self.left_group_box,0,0)

        self.left_group_box.setFixedWidth(180)

        self.variable_1_label = QLabel("Data")
        self.variable_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_group_box_layout.addWidget(self.variable_1_label,0,0)

        self.variable_1_input = QTextEdit()
        self.variable_1_input.setPlaceholderText("Seperated with comma")
        self.left_group_box_layout.addWidget(self.variable_1_input,1,0)

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

        self.right_group_box.setFixedWidth(225)

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

        self.variable_1_input.textChanged.connect(self.reset_and_update_display)


    def reset_and_update_display(self):
        self.current_result = "<span style='color: gray;'><i>Waiting...</i></span>"
        self.update_formula_display()


    def update_formula_display(self):
            
        raw_text = self.variable_1_input.toPlainText().strip()
        if not raw_text:
                self.variable_1 = "&mu;"
                self.variable_2 = "N"
            
        else : 
            try:
                self.data = [float(x.strip()) for x in raw_text.split(",") if x.strip()]
                self.variable_2 = len(self.data)
                self.variable_1 = sum(self.data)
                
            except ValueError:
                self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"
                self.variable_1 = "&mu;"
                self.variable_2 = "N"
    
            
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
                                    &Sigma;(x<sub>i</sub> - {self.variable_1})<sup>2</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 8px 0px 8px;">
                                    {self.variable_2}
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
                result = sum((x - (sum(self.data) / self.variable_2)) ** 2 for x in self.data)/self.variable_2

                self.current_result = f"<span style='color: #10B981; font-weight: bold;'>{result:.4f}</span>"

        except TypeError:
            self.current_result = "<span style='color: #EF4444; font-size: 20px;'>Invalid Input!</span>"

        except AttributeError:
             self.current_result = "<span style='color: #EF4444; font-size: 20px;'>No Data!</span>"
        self.update_formula_display()



        