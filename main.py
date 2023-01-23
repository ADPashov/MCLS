
from mcls_main import MclsMain
# pyinstaller --onefile -w  --path venv\Lib\site-packages --add-data="Model\*;." --add-data="View\*;." --add-data="Controller\*;."  --add-data "C:/Users/ppash/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter;customtkinter/"--icon=mc_logo.ico main.py --hidden-import tkiner  --hidden-import=customtkinter --hidden-import=tkcalendar --hidden-import=babel.numbers

if __name__ == "__main__":
    controller = MclsMain()
