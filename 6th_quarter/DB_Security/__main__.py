import os, platform
from AC06.code import main as AC06

os.system('cls') if platform.system() == 'Windows' else os.system('clear')

# ===== Ejecución de código AC06
ac06 = AC06()
ac06.main()

