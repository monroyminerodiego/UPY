import os
import pandas as pd
import numpy as np
from typing import Literal, Any

from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

class Cleaner:
    def __init__(self, file_path: str | None = None, df: pd.DataFrame | None = None):
        # Manejo de archivo o DataFrame
        if isinstance(df, pd.DataFrame):
            self.df = df.copy()
        elif file_path:
            self.df = pd.read_csv(file_path) if '.csv' in file_path else pd.read_excel(file_path)
        else:
            raise RuntimeError("Se espera que se pase una ruta de archivo (file_path) o un DataFrame (df) para hacer la limpieza de los datos")
        self.location_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def limpiar_imputacion(self, 
                           tipo: Literal['mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate', 'knn', 'iterative', None] = 'median', 
                           valor: Any = 0):
        """
        Imputa los valores faltantes del DataFrame usando distintas estrategias.
        Si 'tipo' es None, elimina las filas que contienen NaN.
        
        Parámetros:
            tipo (str | None): Método de imputación o None para eliminar NaN.
            valor (Any): Valor a utilizar en la imputación constante (default=0).
        """
        if tipo is None:
            # Eliminar filas con cualquier NaN
            self.df = self.df.dropna()
        else:
            if tipo == 'mean':
                numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            elif tipo == 'median':
                numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            elif tipo == 'mode':
                numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
                for col in numeric_cols:
                    mode_val = self.df[col].mode()
                    if not mode_val.empty:
                        self.df[col] = self.df[col].fillna(mode_val[0])
            elif tipo == 'constant':
                self.df = self.df.fillna(valor)
            elif tipo == 'ffill':
                self.df = self.df.fillna(method='ffill')
            elif tipo == 'bfill':
                self.df = self.df.fillna(method='bfill')
            elif tipo == 'interpolate':
                self.df = self.df.interpolate()
            elif tipo == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)
            elif tipo == 'iterative':
                imputer = IterativeImputer(random_state=0)
                self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)
            else:
                raise ValueError("Tipo de imputación no reconocido. Use uno de: 'mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate', 'knn', 'iterative'.")
        return self.df

    def limpiar_patron(self, 
                       impute_method: Literal['mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate', None] = 'median', 
                       constant_value: Any = 0) -> pd.DataFrame:
        """
        Limpia el DataFrame considerando patrones de datos faltantes (MAR o MNAR) mediante la creación de indicadores
        de missing y la imputación de valores faltantes.
        Si 'impute_method' es None, elimina las filas que contienen NaN.
        
        Parámetros:
            impute_method (str | None): Método de imputación para columnas numéricas o None para eliminar NaN.
            constant_value (Any): Valor a usar en la imputación constante (por defecto 0).
        
        Retorna:
            pd.DataFrame: DataFrame limpiado.
        """
        if impute_method is None:
            self.df = self.df.dropna()
        else:
            # 1. Crear columnas indicadoras para cada variable con datos faltantes
            for col in self.df.columns:
                if self.df[col].isnull().sum() > 0:
                    self.df[f"{col}_missing"] = self.df[col].isnull().astype(int)
            
            # 2. Imputar los valores faltantes en columnas numéricas usando el método elegido
            numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            
            if impute_method == 'mean':
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            elif impute_method == 'median':
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            elif impute_method == 'mode':
                for col in numeric_cols:
                    mode_val = self.df[col].mode()
                    if not mode_val.empty:
                        self.df[col] = self.df[col].fillna(mode_val[0])
            elif impute_method == 'constant':
                self.df = self.df.fillna(constant_value)
            elif impute_method == 'ffill':
                self.df = self.df.fillna(method='ffill')
            elif impute_method == 'bfill':
                self.df = self.df.fillna(method='bfill')
            elif impute_method == 'interpolate':
                self.df = self.df.interpolate()
            else:
                raise ValueError("Método de imputación no reconocido. Elija uno de: 'mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate'.")
        
        return self.df
