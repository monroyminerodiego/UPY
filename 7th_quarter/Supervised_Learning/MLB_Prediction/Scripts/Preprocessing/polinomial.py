import os, sys,json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

# 2. Crea una nueva clase o modifica la existente
class FeatureTransformer:
    def __init__(self, df: pd.DataFrame | None = None):
        """
        Inicializa el transformador de características.
        
        Parámetros:
            df (pd.DataFrame | None): DataFrame para transformación.
        """
        if isinstance(df, pd.DataFrame):
            self.df = df.copy()
        else:
            raise RuntimeError("Se requiere un DataFrame para transformar las características")
        
        self.location_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    def aplicar_polinomios(self, 
                         grado: int = 2, 
                         incluir_interacciones: bool = True,
                         columnas: list[str] | None = None,
                         excluir: list[str] | None = None) -> pd.DataFrame:
        """
        Aplica transformación polinómica a las columnas seleccionadas.
        
        Parámetros:
            grado (int): Grado máximo de los polinomios (default=2).
            incluir_interacciones (bool): Si se incluyen términos de interacción (default=True).
            columnas (list[str] | None): Lista de columnas a transformar. Si es None, se transforman todas
                                        las columnas numéricas.
            excluir (list[str] | None): Lista de columnas a excluir de la transformación.
            
        Retorna:
            pd.DataFrame: DataFrame con las características polinómicas añadidas.
        """
        # Si no se especifican columnas, seleccionar todas las numéricas
        if columnas is None:
            columnas = list(self.df.select_dtypes(include=['int64', 'float64']).columns)
        
        # Excluir columnas si se indica
        if excluir is not None:
            columnas = [col for col in columnas if col not in excluir]
        
        # Configurar PolynomialFeatures
        interaction_only = not incluir_interacciones
        poly = PolynomialFeatures(degree=grado, include_bias=False, interaction_only=interaction_only)
        
        # Extraer las columnas a transformar
        X_poly = self.df[columnas].values
        
        # Aplicar la transformación
        X_poly_transformed = poly.fit_transform(X_poly)
        
        # Obtener nombres de las nuevas características
        feature_names = poly.get_feature_names_out(columnas)
        
        # Crear un nuevo DataFrame con las características originales y las transformadas
        df_transformado = self.df.copy()
        
        # Quitar las columnas originales que serán reemplazadas
        df_transformado = df_transformado.drop(columns=columnas)
        
        # Añadir las características polinómicas
        for i, name in enumerate(feature_names):
            df_transformado[name] = X_poly_transformed[:, i]
        
        return df_transformado