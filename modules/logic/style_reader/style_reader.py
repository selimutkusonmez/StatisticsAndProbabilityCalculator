import os
from config import STYLE_PATH

def read_style(file_name):
    file_path = os.path.join(STYLE_PATH,file_name)
    
    with open(file_path,"r") as f:
        return f.read()