from termcolor import colored
import os
from datetime import datetime

def create_screenshot_directory():
    current_year = datetime.now().year
    current_month = datetime.now().month
    directory_path = f"screenshots/{current_year}/{current_month}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(colored(f"Directorio creado: {directory_path}",'green'))
    else:
        print(colored(f"El directorio ya existe: {directory_path}",'green'))
    return directory_path

if __name__ == "__main__":
    create_screenshot_directory()