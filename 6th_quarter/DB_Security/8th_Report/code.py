import os, sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))
from Manager.db import database_manager

class AC09:

    def __init__(self):
        self.conexion = None

    def api_configuration(self):
        print(f"\n{'='*5} API Configuration")
        self.conexion = database_manager()

    def main(self):
        ''' 
        '''