import os
import numpy as np
import pandas as pd
from math import sqrt
from sklearn.linear_model import SGDRegressor, LinearRegression
from sklearn.metrics import mean_squared_error
from typing import Literal, Optional

class ModeloRegresionLineal:
    def __init__(self,
                 gd_type: Literal[None, 'stochastic', 'mini-batch', 'batch'] = 'stochastic',
                 regularizacion: Literal['ridge', 'lasso', 'elasticnet', None] = None,
                 learning_rate: float = 0.01,
                 epochs: int = 100,
                 batch_size: Optional[int] = 20):
        """
        Inicializa la clase para probar modelos de regresión lineal.

        Parámetros:
            gd_type (None o str): Si es None se usa un método analítico (sin descenso de gradiente),
                                   de lo contrario se usa descenso de gradiente ('stochastic', 'mini-batch' o 'batch').
            regularizacion (str): Tipo de regularización ('ridge', 'lasso', 'elasticnet', 'none').
            learning_rate (float): Tasa de aprendizaje para el descenso de gradiente.
            epochs (int): Número de épocas de entrenamiento.
            batch_size (int | None): Tamaño del batch para mini-batch (se usa solo si gd_type es 'mini-batch').
        """
        self.gd_type = gd_type
        self.regularizacion = regularizacion
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.location_path = os.path.dirname(os.path.dirname(__file__))

    def __configurar_modelo(self):
        """
        Configura y genera el modelo de regresión lineal según la configuración seleccionada.
        
        Si gd_type es None, se utiliza LinearRegression (solución analítica) y se eliminarán
        filas con valores faltantes antes del ajuste.
        En caso contrario, se utiliza SGDRegressor configurado para entrenamiento manual.
        """
        if self.gd_type is None:
            # No se usa descenso de gradiente, se utiliza un modelo analítico.
            self.model = LinearRegression()
        else:
            # Mapear la regularización a la penalización correspondiente
            if self.regularizacion == 'ridge':
                penalty = 'l2'
            elif self.regularizacion == 'lasso':
                penalty = 'l1'
            elif self.regularizacion == 'elasticnet':
                penalty = 'elasticnet'
            else:
                penalty = None
            
            # Configurar el modelo con SGDRegressor para usar descenso de gradiente
            self.model = SGDRegressor(loss='squared_error',  # Error cuadrático para regresión
                                      penalty=penalty,
                                      learning_rate='constant',
                                      eta0=self.learning_rate,
                                      max_iter=1,            # Se entrena en loop manual (una iteración por llamada a partial_fit)
                                      warm_start=True,       # Permite continuar entrenando sobre el mismo modelo
                                      shuffle=False,         # Se controla la mezcla de datos en el loop externo
                                      random_state=42)

    def entrenar_modelo(self, X, y):
        """
        Entrena el modelo utilizando descenso de gradiente si gd_type no es None.
        Si gd_type es None, se ajusta el modelo de forma directa (sin iteraciones de descenso)
        eliminando previamente las filas con valores faltantes.

        Parámetros:
            X (array-like o pd.DataFrame): Variables predictoras.
            y (array-like o pd.Series): Variable a predecir.

        Retorna:
            self.model: Modelo entrenado.
        """
        # Configurar el modelo si aún no se ha hecho
        if self.model is None:
            self.__configurar_modelo()
        
        # Convertir a arrays de numpy
        X = np.array(X)
        y = np.array(y)

        if self.gd_type is None:
            # Eliminamos filas que tengan al menos un NaN para que LinearRegression pueda ajustarse
            df_fit = pd.DataFrame(X, columns=[f"col{i}" for i in range(X.shape[1])])
            df_fit['target'] = y
            df_fit = df_fit.dropna()
            X_fit = df_fit.drop(columns=['target']).values
            y_fit = df_fit['target'].values
            self.model.fit(X_fit, y_fit)
        else:
            n_samples = X.shape[0]
            # Determinar el tamaño del batch según el tipo de descenso
            if self.gd_type == 'stochastic':
                batch_size = 1
            elif self.gd_type == 'batch':
                batch_size = n_samples
            elif self.gd_type == 'mini-batch':
                batch_size = self.batch_size if self.batch_size is not None else 32
            else:
                raise ValueError("gd_type no reconocido. Use 'stochastic', 'mini-batch', 'batch' o None.")
            
            # Loop de entrenamiento por épocas
            for epoch in range(self.epochs):
                # Mezclar los datos al inicio de cada época
                indices = np.arange(n_samples)
                np.random.shuffle(indices)
                X_shuffled = X[indices]
                y_shuffled = y[indices]
                # Dividir en batches y actualizar el modelo para cada uno
                for start in range(0, n_samples, batch_size):
                    end = start + batch_size
                    X_batch = X_shuffled[start:end]
                    y_batch = y_shuffled[start:end]
                    self.model.partial_fit(X_batch, y_batch)
        
        return self.model

    def predecir(self, X):
        """
        Realiza predicciones utilizando el modelo entrenado y agrega la columna de predicciones a X.

        Parámetros:
            X (array-like o pd.DataFrame): Datos de entrada para la predicción.

        Retorna:
            pd.DataFrame: El mismo DataFrame X con una nueva columna 'R_pred' que contiene las predicciones.
        """
        if self.model is None:
            raise RuntimeError("El modelo no ha sido configurado o entrenado.")
        
        predictions = self.model.predict(np.array(X))
        
        if isinstance(X, pd.DataFrame):
            X_copy = X.copy()
            X_copy['R_pred'] = predictions
            return X_copy
        else:
            X_df = pd.DataFrame(X)
            X_df['R_pred'] = predictions
            return X_df
    
    def evaluar(self, df: pd.DataFrame, columna_real: str = 'R', columna_pred: str = 'R_pred') -> float:
        """
        Evalúa el modelo calculando el RMSE (Root Mean Squared Error) a partir de un DataFrame que ya contiene las predicciones.

        Parámetros:
            df (pd.DataFrame): DataFrame que contiene la columna con las predicciones y la columna con los valores reales.
            columna_real (str): Nombre de la columna con los valores reales (por defecto 'R').
            columna_pred (str): Nombre de la columna con las predicciones (por defecto 'R_pred').

        Retorna:
            float: Valor del RMSE.
        """
        if columna_pred not in df.columns:
            raise ValueError(f"El DataFrame no contiene la columna de predicción '{columna_pred}'.")
        if columna_real not in df.columns:
            raise ValueError(f"El DataFrame no contiene la columna de valores reales '{columna_real}'.")
        
        y_pred = df[columna_pred]
        y_true = df[columna_real]
        rmse = sqrt(mean_squared_error(y_true, y_pred))
        return rmse
