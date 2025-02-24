import os
import pandas as pd
from typing import Literal, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler

class Normalizer:
    def __init__(self, file_path: str | None = None, df: pd.DataFrame | None = None):
        """
        Inicializa el normalizador a partir de un archivo o de un DataFrame.
        
        Parámetros:
            file_path (str | None): Ruta al archivo (.csv o .xlsx).
            df (pd.DataFrame | None): DataFrame ya cargado.
            guardar_output (bool): Si es True, guarda el DataFrame transformado en disco.
        """
        if isinstance(df, pd.DataFrame):  self.df = df.copy()
        elif file_path:                   self.df = pd.read_csv(file_path) if '.csv' in file_path else pd.read_excel(file_path)
        else:                             raise RuntimeError("Se espera que se pase una ruta de archivo (file_path) o un DataFrame (df) para hacer la normalización de los datos")
        
        self.location_path  = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def normalizar_datos(self, 
                         tipo: Literal[None,'standard', 'minmax', 'maxabs', 'robust'] = 'standard', 
                         columnas: list[str] | None = None,
                         excluir: list[str] | None = None) -> pd.DataFrame:
        """
        Normaliza (escala) las columnas del DataFrame utilizando distintos escaladores.

        Parámetros:
            tipo (str): Tipo de escalador a utilizar. Opciones:
                - 'standard': StandardScaler, transforma los datos a media 0 y desviación estándar 1.
                - 'minmax': MinMaxScaler, escala los valores al rango [0, 1].
                - 'maxabs': MaxAbsScaler, escala los datos en función del valor absoluto máximo.
                - 'robust': RobustScaler, utiliza la mediana y el rango intercuartílico para la escalación.
            columnas (list[str] | None): Lista de nombres de columnas a normalizar. Si es None, se normalizan todas
                                          las columnas numéricas.
            excluir (list[str] | None): Lista de columnas a excluir de la normalización (por ejemplo, la variable objetivo).

        Retorna:
            pd.DataFrame: DataFrame con las columnas normalizadas.
        """
        if tipo != None:
            # Si no se especifican columnas, se seleccionan todas las columnas numéricas
            if columnas is None: columnas = list(self.df.select_dtypes(include=['int64', 'float64']).columns)
            
            # Se excluyen columnas si se indica
            if excluir is not None: columnas = [col for col in columnas if col not in excluir]
            
            # Seleccionar el escalador según el parámetro 'tipo'
            if tipo == 'standard': scaler = StandardScaler()
            elif tipo == 'minmax': scaler = MinMaxScaler()
            elif tipo == 'maxabs': scaler = MaxAbsScaler()
            elif tipo == 'robust': scaler = RobustScaler()
            else:                  raise ValueError("Tipo de normalización no reconocido. Use uno de: 'standard', 'minmax', 'maxabs', 'robust'.")
            
            # Aplicar el escalador a las columnas seleccionadas
            self.df[columnas] = scaler.fit_transform(self.df[columnas])
        
                
        return self.df
