import os, sys,json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

from .Preprocessing.clean_data import Cleaner
from .Predictions.linear_regression import ModeloRegresionLineal
from .Preprocessing.normalize_data import Normalizer
from .Preprocessing.standard_data import Standardizer
from .Preprocessing.polinomial import FeatureTransformer

class Pipeline:
    def __init__(self):
        ''' 
        '''
        self.location_path = os.path.dirname(os.path.dirname(__file__))
        
        file_path = os.path.join(self.location_path,"Files","Data","Transformed","predictions.json")
        with open(file_path,'r') as file: self.pipe_data = json.load(file)

    def __obtener_dataframes(self):
        ''' 
        '''
        # ===== Raw - train data
        raw_data_path = os.path.join(self.location_path,'Files','Data','Raw','train.csv')
        df = pd.read_csv(raw_data_path)

        # ===== Raw - predict data
        raw_data_path = os.path.join(self.location_path,'Files','Data','Raw','prediction.csv')
        df_predict = pd.read_csv(raw_data_path)

        return df, df_predict
    
    def __guardar_combinacion(self,nombre:str,resultado:float):
        file_path = os.path.join(self.location_path,"Files","Data","Transformed","predictions.json")
        if not(os.path.isfile(file_path)):
            with open(file_path,'w') as file: json.dump({},file,ensure_ascii=False,indent=4)
        
        with open(file_path,'r') as file: self.pipe_data = json.load(file)
        self.pipe_data[nombre] = resultado
        with open(file_path,'w') as file: json.dump(self.pipe_data,file,ensure_ascii=False,indent=4)

    def intentar_combinaciones_imputacion(self,resultados:dict = {},norm:bool = True):
        '''
        '''
        df_unchanged, df_predict_unchanged = self.__obtener_dataframes()

        # ===== Limpieza Imputacion / Estandarizacion / Normalizacion
        nombre_config_init = f"I."
        for key_l,tipo_limpieza in {'A': None, 'B': 'mean', 'C': 'median', 'D': 'mode', 'E': 'constant', 'F': 'ffill', 'G': 'bfill', 'H': 'interpolate', 'I': 'knn', 'J': 'iterative'}.items():
            print(f'\n')
            nombre_config_L = f"{nombre_config_init}{key_l}-"
            df_l = Cleaner(df = df_unchanged).limpiar_imputacion(tipo_limpieza)
        
            # ===== Estandarizacion
            nombre_config_L += f"E.{'1' if norm else '0'}-"
            if norm: df_l = Standardizer(df = df_l).estandarizar_datos(excluir=['R','Id','yearID'])

            # ====== Normalizacion
            for key_n,tipo_normalizacion in {'A':None,'B':'standard', 'C':'minmax', 'D':'maxabs', 'E':'robust'}.items():
                nombre_config_N = f"{nombre_config_L}N.{key_n}-"
                df_n = Normalizer(df = df_l).normalizar_datos(tipo_normalizacion,excluir=['R','Id','yearID'])

                # ===== Data Procesada
                X = df_n.drop(columns=['R'])
                y = df_n['R']
                X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.2)

                # ====== Gradient Descent
                for key_g, tipo_gradient in {'A':None,'B':'stochastic', 'C':'mini-batch', 'D':'batch'}.items():
                    nombre_config_G = f"{nombre_config_N}G.{key_g}-"
                    
                    # ===== Regularization
                    for key_r, tipo_regularizacion in {'A':None,'B':'ridge', 'C':'lasso', 'D':'elasticnet'}.items():
                        nombre_config_R = f"{nombre_config_G}R.{key_r}"


                        # ====== Modelo
                        if not(nombre_config_R in self.pipe_data):
                            modelo = ModeloRegresionLineal(
                                gd_type = tipo_gradient,
                                regularizacion = tipo_regularizacion
                            )

                            modelo.entrenar_modelo(X_train,y_train)

                            prediccion = modelo.predecir(X_dev)
                            prediccion['R'] = y_dev.values

                            error = modelo.evaluar(prediccion)

                            print(f"{nombre_config_R}:   '{error}'")
                            resultados[nombre_config_R] = error
                            self.__guardar_combinacion(nombre_config_R,error)

        return resultados
    
    def intentar_combinaciones_patron(self,resultados:dict = {},norm:bool = True):
        '''
        '''
        df_unchanged, df_predict_unchanged = self.__obtener_dataframes()

        # ===== Limpieza Patron / Estandarizacion / Normalizacion
        nombre_config_init = f"P."
        for key_l,tipo_limpieza in {'A': None, 'B': 'mean', 'C': 'median', 'D': 'mode', 'E': 'constant', 'F': 'ffill', 'G': 'bfill', 'H': 'interpolate'}.items():
            nombre_config_L = f"{nombre_config_init}{key_l}-"
            df = Cleaner(df = df_unchanged).limpiar_patron(tipo_limpieza)
        
            # ===== Estandarizacion
            nombre_config_L += f"E.{'1' if norm else '0'}-"
            if norm: df = Standardizer(df = df).estandarizar_datos(excluir=['R','Id','yearID'])

            # ====== Normalizacion
            for key_n,tipo_normalizacion in {'A':None,'B':'standard', 'C':'minmax', 'D':'maxabs', 'E':'robust'}.items():
                nombre_config_N = f"{nombre_config_L}N.{key_n}-"
                df = Normalizer(df = df).normalizar_datos(tipo_normalizacion,excluir=['R','Id','yearID'])

                # ===== Data Procesada
                X = df.drop(columns=['R'])
                y = df['R']
                X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.2)

                # ====== Gradient Descent
                for key_g, tipo_gradient in {'A':None,'B':'stochastic', 'C':'mini-batch', 'D':'batch'}.items():
                    nombre_config_G = f"{nombre_config_N}G.{key_g}-"
                    
                    # ===== Regularization
                    for key_r, tipo_regularizacion in {'A':None,'B':'ridge', 'C':'lasso', 'D':'elasticnet'}.items():
                        nombre_config_R = f"{nombre_config_G}R.{key_r}"


                        # ====== Modelo
                        if not(nombre_config_R in self.pipe_data):
                            modelo = ModeloRegresionLineal(
                                gd_type = tipo_gradient,
                                regularizacion = tipo_regularizacion
                            )

                            modelo.entrenar_modelo(X_train,y_train)

                            prediccion = modelo.predecir(X_dev)
                            prediccion['R'] = y_dev.values

                            error = modelo.evaluar(prediccion)

                            print(f"{nombre_config_R}:   '{error}'")
                            resultados[nombre_config_R] = error
                            self.__guardar_combinacion(nombre_config_R,error)

        return resultados
    
    def intentar_combinaciones_personalizado(self,combinaciones:list[str],polinomial:bool = False):
        '''
        '''
        df_unchanged, df_predict_unchanged = self.__obtener_dataframes()
        errores = {}
        for combinacion_completa in combinaciones:
            print(f"{combinacion_completa}:    ",end = '')
            combinacion = combinacion_completa.split('-')

            # ===== Diccionarios deficiones
            tipo_limpieza       = {'A':None, 'B':'mean',       'C':'median',     'D':'mode',   'E':'constant', 'F':'ffill', 'G':'bfill', 'H':'interpolate', 'I':'knn', 'J':'iterative'}
            tipo_normalizacion  = {'A':None, 'B':'standard',   'C':'minmax',     'D':'maxabs', 'E':'robust'}
            tipo_gradient       = {'A':None, 'B':'stochastic', 'C':'mini-batch', 'D':'batch'}
            tipo_regularizacion = {'A':None, 'B':'ridge',      'C':'lasso',      'D':'elasticnet'}

            # ==== Data Preprocessing
            # Limpieza
            key_l = combinacion[0].split('.')
            if   key_l[0] == 'I': df_l = Cleaner(df = df_unchanged).limpiar_imputacion(tipo = tipo_limpieza[key_l[1]])
            elif key_l[0] == 'P': df_l = Cleaner(df = df_unchanged).limpiar_patron(impute_method = tipo_limpieza[key_l[1]])

            if polinomial:
                df_n = FeatureTransformer(df = df_l).aplicar_polinomios(excluir=['R', 'Id', 'yearID'])
            
            else:
                # Estandarizacion 
                key_e = bool(combinacion[1].split('.')[1])
                if key_e: df_l = Standardizer(df = df_l).estandarizar_datos(excluir=['R','Id','yearID'])

                # Normalizacion
                key_n = combinacion[2].split('.')[1]
                df_n = Normalizer(df = df_l).normalizar_datos(tipo = tipo_normalizacion[key_n],excluir=['R','Id','yearID'])

            # Split
            X = df_n.drop(columns=['R'])
            y = df_n['R']
            X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size=0.2)

            # ====== Model config
            # Gradient Descent
            key_g = combinacion[3].split('.')[1]

            # Regularization
            key_r = combinacion[4].split('.')[1]

            modelo = ModeloRegresionLineal(
                gd_type = tipo_gradient[key_g],
                regularizacion = tipo_regularizacion[key_r]
            )

            modelo.entrenar_modelo(X_train,y_train)

            # Model dev
            prediccion_dev = modelo.predecir(X_dev)
            prediccion_dev['R'] = y_dev.values
            error = modelo.evaluar(prediccion_dev)
            print(f"{error}")

            # ===== Model test - Data preparation
            # Limpieza
            key_l = combinacion[0].split('.')
            if   key_l[0] == 'I': df_l = Cleaner(df = df_predict_unchanged).limpiar_imputacion(tipo = tipo_limpieza[key_l[1]])
            elif key_l[0] == 'P': df_l = Cleaner(df = df_predict_unchanged).limpiar_patron(impute_method = tipo_limpieza[key_l[1]])

            # Estandarizacion 
            key_e = bool(combinacion[1].split('.')[1])
            if key_e: df_l = Standardizer(df = df_l).estandarizar_datos(excluir=['R','Id','yearID'])

            # Normalizacion
            key_n = combinacion[2].split('.')[1]
            df_n = Normalizer(df = df_l).normalizar_datos(tipo = tipo_normalizacion[key_n],excluir=['R','Id','yearID'])

            prediccion_test = modelo.predecir(df_n)
            prediccion_test = prediccion_test[['Id','R_pred']]
            prediccion_test.columns = ['Id','R']
            prediccion_test['Id'] = prediccion_test['Id'].astype(int)

            save_path = os.path.join(self.location_path,'Files','Outputs',f'{combinacion_completa.replace('.','').replace('-','_')}.csv')
            prediccion_test.to_csv(save_path,index=False)


    def main(self):
        ''' 
        '''

        # ===== Mejores Combinaciones
        combinaciones = [
            'I.A-E.1-N.A-G.A-R.A',
            'I.A-E.1-N.B-G.A-R.A',
            'I.A-E.1-N.C-G.A-R.A',
            'I.A-E.1-N.D-G.A-R.A',
            'I.A-E.1-N.E-G.A-R.A',
            'I.C-E.1-N.A-G.A-R.A',
            'I.D-E.1-N.D-G.A-R.A',
            'I.E-E.1-N.A-G.A-R.A',
            'I.E-E.1-N.B-G.A-R.A',
            'I.E-E.1-N.C-G.A-R.A',
            'I.E-E.1-N.D-G.A-R.A',
            'I.E-E.1-N.E-G.A-R.A',
            'I.G-E.1-N.A-G.A-R.A',
            'I.I-E.1-N.A-G.A-R.A',
            'I.I-E.1-N.B-G.A-R.A',
            'I.I-E.1-N.C-G.A-R.A',
            'I.I-E.1-N.D-G.A-R.A',
            'I.I-E.1-N.E-G.A-R.A',
            'I.J-E.1-N.A-G.A-R.A',
            'I.J-E.1-N.B-G.A-R.A',
            'I.J-E.1-N.C-G.A-R.A',
            'I.J-E.1-N.D-G.A-R.A',
            'I.J-E.1-N.E-G.A-R.A'
        ]
        

        combinaciones_final = []
        for combinacion in combinaciones:
            if not('I.I' in combinacion) and not('I.J' in combinacion): combinacion = combinacion.replace('I.','P.')
            combinacion = combinacion.replace('E.1','E.0')
            combinaciones_final.append(combinacion)
        combinaciones_final += combinaciones


        print(f"Hay {len(combinaciones_final)} combinaciones...")

        results = self.intentar_combinaciones_personalizado(combinaciones_final)

        print(results.head(18))
        

        print("\n\nTermino de evaluar")

