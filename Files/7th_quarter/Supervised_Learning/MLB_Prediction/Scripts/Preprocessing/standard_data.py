import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import List, Union

class Standardizer:
    def __init__(self, file_path: Union[str, None] = None, df: Union[pd.DataFrame, None] = None):
        """
        Inicializa la clase Estandarizador a partir de un archivo o de un DataFrame.

        Parámetros:
            file_path (str | None): Ruta al archivo (.csv o .xlsx) que contiene los datos.
            df (pd.DataFrame | None): DataFrame ya cargado.
            guardar_output (bool): Si True, guarda el DataFrame transformado en disco.
        """
        if isinstance(df, pd.DataFrame):  self.df = df.copy()
        elif file_path:                   self.df = pd.read_csv(file_path) if '.csv' in file_path else pd.read_excel(file_path)
        else:                             raise RuntimeError("Se debe proporcionar un file_path o un DataFrame para la estandarización de datos")
        
        self.location_path = os.path.dirname(os.path.dirname(__file__))

    def estandarizar_datos(self, columnas: Union[List[str], None] = None, excluir: Union[List[str], None] = None) -> pd.DataFrame:
        """
        Estandariza (transforma a media 0 y desviación estándar 1) las columnas numéricas seleccionadas.

        Parámetros:
            columnas (list[str] | None): Lista de nombres de columnas a estandarizar. 
                                          Si es None, se seleccionan todas las columnas numéricas.
            excluir (list[str] | None): Lista de columnas a excluir de la estandarización (por ejemplo, la variable objetivo).

        Retorna:
            pd.DataFrame: DataFrame con las columnas estandarizadas.
        """
        # Si no se especifican columnas, se seleccionan todas las columnas numéricas
        if columnas is None: columnas = list(self.df.select_dtypes(include=['int64', 'float64']).columns)
        
        # Excluir columnas si se indica
        if excluir is not None: columnas = [col for col in columnas if col not in excluir]
        
        # Crear el objeto StandardScaler y ajustar-transformar las columnas seleccionadas
        scaler = StandardScaler()
        self.df[columnas] = scaler.fit_transform(self.df[columnas])
        
                
        return self.df
