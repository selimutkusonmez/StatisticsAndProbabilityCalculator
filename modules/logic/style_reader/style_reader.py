import os
from config import STYLE_PATH

def read_style(current_theme,font_size,font_color):
    if current_theme == "dark":
        file_name = "main_ui_dark_theme.qss"
    else:
        file_name = "main_ui_light_theme.qss"

    file_path = os.path.join(STYLE_PATH,file_name)
    
    with open(file_path,"r") as f:
        qss_content = f.read()

    dynamic_qss = qss_content.replace("{FONT_SIZE}",str(font_size))
    dynamic_qss = dynamic_qss.replace("{FONT_COLOR}",str(font_color))

    return dynamic_qss
    
