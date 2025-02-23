import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Literal, Any

from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

class Cleaner:

    def __init__(self,file_path:str|None = None,df:pd.DataFrame|None = None,
                 guardar_output:bool = False):
        
        # Manejo archivo
        if df:           self.df = df
        elif file_path:  self.df = pd.read_csv(file_path) if '.csv' in file_path else pd.read_excel(file_path)
        else:            raise RuntimeError("Se espera que se pase una ruta de archivo (file_path) o un DataFrame (df) para hacer la limpieza de los datos")

        self.location_path  = os.path.dirname(os.path.dirname(__file__))
        self.guardar_output = guardar_output

    def limpiar_imputacion(self, 
                           tipo: Literal['mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate', 'knn', 'iterative'] = 'median', 
                           valor: Any = 0):
        """
        Imputa los valores faltantes del DataFrame usando distintas estrategias.

        Parámetros:
            tipo (str): Método de imputación. Puede ser:
                - 'mean': Imputa con la media.
                - 'median': Imputa con la mediana.
                - 'mode': Imputa con la moda (valor más frecuente).
                - 'constant': Imputa con un valor constante (definido en 'valor').
                - 'ffill': Imputa usando forward fill (propaga el último valor no nulo).
                - 'bfill': Imputa usando backward fill (propaga el siguiente valor no nulo).
                - 'interpolate': Imputa usando interpolación lineal.
                - 'knn': Imputa usando KNNImputer de sklearn (n_neighbors=5 por defecto).
                - 'iterative': Imputa usando IterativeImputer de sklearn.
            valor (Any): Valor a utilizar en la imputación constante (default=0).

        Nota:
            Algunos métodos (como knn o iterative) requieren que todas las columnas sean numéricas o que se hayan tratado
            las columnas no numéricas por separado.
        """
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
            # Se reconstruye el DataFrame a partir de la imputación (solo para datos numéricos)
            self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)

        elif tipo == 'iterative':
            imputer = IterativeImputer(random_state=0)
            self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)

        else:
            raise ValueError("Tipo de imputación no reconocido. Use uno de: 'mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate', 'knn', 'iterative'.")

        if self.guardar_output: self.df.to_csv(os.path.join(
                self.location_path,
                "Files",
                "Data",
                "Transformed",
                f"train_imputacion_{tipo}.csv"
            ))

        return self.df

    def limpiar_patron(self, 
                       impute_method: Literal['mean', 'median', 'mode', 'constant', 'ffill', 'bfill', 'interpolate'] = 'median', 
                       constant_value: Any = 0) -> None:
        """
        Limpia el DataFrame considerando patrones de datos faltantes (MAR o MNAR) mediante la creación de indicadores
        de missing y la imputación de valores faltantes.
        
        Parámetros:
            impute_method (str): Método de imputación para columnas numéricas. Opciones:
                - 'mean': Imputa con la media.
                - 'median': Imputa con la mediana (recomendado para datos asimétricos).
                - 'mode': Imputa con la moda.
                - 'constant': Imputa con un valor constante, definido en constant_value.
                - 'ffill': Imputa utilizando forward fill.
                - 'bfill': Imputa utilizando backward fill.
                - 'interpolate': Imputa mediante interpolación lineal.
            constant_value (Any): Valor a usar en la imputación constante (por defecto 0).
        
        Procedimiento:
            1. Se añaden, para cada columna con valores faltantes, una nueva columna indicadora con el sufijo '_missing'
               que contiene 1 si el dato estaba ausente y 0 si no.
            2. Se aplica el método de imputación especificado a las columnas numéricas.
        """
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
        
        if self.guardar_output: self.df.to_csv(os.path.join(
                self.location_path,
                "Files",
                "Data",
                "Transformed",
                f"train_patron_{impute_method}.csv"
            ))

        return self.df

if __name__ == '__main__':
    os.system('clear')

    cleaner1 = Cleaner(
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'Files',
            'Data',
            'Raw',
            'train.csv'
        )
    ).limpiar_imputacion()
    print(cleaner1.info())

    print('\n\n\n')

    cleaner2 = Cleaner(
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'Files',
            'Data',
            'Raw',
            'train.csv'
        )
    ).limpiar_patron()
    print(cleaner2.info())


