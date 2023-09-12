"""
Comando para ejecutar este script:
$ python3 main.py
"""


# Importo mi clase
from ClassCar import DataBase

#Creo mi DB
DB = DataBase([["carro 1", 100, 180, 4, 4 ],["carro 2", 200, 180, 4, 4 ],["carro 3", 200, 180, 4, 4 ]])


# Mostrar Autos (descomenta solo esta linea)
#DB.ShowCars()


# Añadir Autos (descomenta solo estas 3 lineas)
#DB.ShowCars()
#DB.AddCar()
#DB.ShowCars()


# Borrar Autos (Descomenta estas dos lineas)
#DB.DeleteCar()
#DB.ShowCars()

# Buscar un auto info (Descomenta esta)
#DB.ShowCar()
