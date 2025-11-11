import os, argparse, platform
import pandas as pd, numpy as np
from typing import Literal
from sklearn.preprocessing import StandardScaler

# ===== Limpia la terminal dependiendo el OS
if platform.system() == 'Windows': os.system('cls')
elif platform.system() == 'Linux': os.system('clear')

# ===== Procesamiento de Argumentos
parser = argparse.ArgumentParser()
parser.add_argument('--tipoProcesamiento', default='reg_logistica', type=str, help="Indica qué tipo de procesamiento seguir: ['reg_logistica','arboles','ensamble','red_neuronal']")
args = parser.parse_args()

# ===== Clase para procesamiento de data
class PreprocesarData:
    # =============== CONSTRUCTOR ===============
    def __init__(self,tipo_procesamiento:Literal['reg_logistica','arboles','ensamble','red_neuronal']):
        
        self.location_path = os.path.dirname(os.path.dirname(__file__))
        self.tipo_procesamiento = tipo_procesamiento
        


    # =============== METODOS PRIVADOS ===============
    # ===== General
    def __cargar_dataframe(self):
        print('Cargando Dataframe...')
        # ===== Lectura de Data
        file_path = os.path.join(self.location_path,'Data','raw','german.data')
        with open(file_path,'r') as file:
            lines = [line.replace('\n','').split(' ') for line in file]

        # ===== Creacion de DataFrame
        self.dataframe = pd.DataFrame(
            data = lines,
            columns = [
                'status_checking_account', # 1.  cualitative
                'month_credit_duration',   # 2.  numeric
                'credit_history',          # 3.  cualitative
                'purpose',                 # 4.  cualitative
                'credit_amount',           # 5.  numeric
                'savings_type',            # 6.  cualitative
                'years_of_employment',     # 7.  cualitative
                'pct_fee_income',          # 8.  numeric
                'status_sex',              # 9.  cualitative
                'debtors',                 # 10. cualitative
                'years_of_residence',      # 11. numeric
                'property',                # 12. cualitative
                'age',                     # 13. numeric
                'other_installments',      # 14. cualitative
                'housing',                 # 15. cualitative
                'num_existing_credits',    # 16. numeric
                'job',                     # 17. cualitative
                'num_dependents',          # 18. numeric
                'telephone',               # 19. cualitative
                'foreign_worker',          # 20. cualitative
                'target'                   # 21. (1 = Good, 2 = Bad)
            ]
        )

        self.dataframe['target'] = self.dataframe['target'].str.replace('2','0')

    def __validar_tipos_de_dato(self):
        print('\tValidando tipos de dato numerico...')
        self.dataframe['month_credit_duration'] = self.dataframe['month_credit_duration'].astype(int)
        self.dataframe['credit_amount']         = self.dataframe['credit_amount'].astype(int)
        self.dataframe['age']                   = self.dataframe['age'].astype(int)
        self.dataframe['pct_fee_income']        = self.dataframe['pct_fee_income'].astype(int)
        self.dataframe['years_of_residence']    = self.dataframe['years_of_residence'].astype(int)
        self.dataframe['num_existing_credits']  = self.dataframe['num_existing_credits'].astype(int)
        self.dataframe['num_dependents']        = self.dataframe['num_dependents'].astype(int)
        self.dataframe['target']                = self.dataframe['target'].astype(int)

    def __guardar_dataframe(self):
        print('Guardando dataframe...')
        self.dataframe.to_csv(
            os.path.join(self.location_path,'Data','processed',f'data_preprocesada_{self.tipo_procesamiento}.csv'),
            index = False
        )

    def __explicar_dataframe(self):
        print('\tEl dataframe está así:')
        index = 1
        for column in self.dataframe.columns: 
            text = f"{index}.- {column}:"
            if len(text) < 40: text = f"{text}{' '*(40-len(text))}"
            print(f"\t\t{text}{sorted(list(set(self.dataframe[column]))[:5])}")
            index += 1

    def __cambiar_nomenclaturas(self):
        print('\tCambiando dataframe para que sea más interpretativo...')
        self.dataframe['status_checking_account'] = self.dataframe['status_checking_account'   ].str.replace('A11','low'    ).str.replace('A12','mid'          ).str.replace('A13','high'         ).str.replace('A14','low')
        self.dataframe['credit_history']          = self.dataframe['credit_history'            ].str.replace('A30','warning').str.replace('A31','good'         ).str.replace('A32','good'         ).str.replace('A33','warning'      ).str.replace('A34','critical')
        self.dataframe['purpose']                 = self.dataframe['purpose'                   ].str.replace('A410','others').str.replace('A40','durable-goods').str.replace('A41','durable-goods').str.replace('A42','durable-goods').str.replace('A43','durable-goods').str.replace('A44','durable-goods').str.replace('A45','business').str.replace('A46','education').str.replace('A47','others').str.replace('A48','education').str.replace('A49','business')
        self.dataframe['savings_type']            = self.dataframe['savings_type'              ].str.replace('A61','low'    ).str.replace('A62','mid'          ).str.replace('A63','high'         ).str.replace('A64','high'         ).str.replace('A65','low')
        self.dataframe['years_of_employment']     = self.dataframe['years_of_employment'       ].str.replace('A71','jr'     ).str.replace('A72','jr'           ).str.replace('A73','md'           ).str.replace('A74','md'           ).str.replace('A75','sr')
        self.dataframe['status_sex']              = self.dataframe['status_sex'                ].str.replace('A91','male'   ).str.replace('A93','male'         ).str.replace('A94','male'         ).str.replace('A92','female'       ).str.replace('A95','female')
        self.dataframe['debtors']                 = self.dataframe['debtors'                   ].str.replace('A101','none'  ).str.replace('A102','co-applicant').str.replace('A103','guarantor')
        self.dataframe['property']                = self.dataframe['property'                  ].str.replace('A121','high'  ).str.replace('A122','mid'         ).str.replace('A123','mid'         ).str.replace('A124','low')
        self.dataframe['housing']                 = self.dataframe['housing'                   ].str.replace('A151','rent'  ).str.replace('A152','own'         ).str.replace('A153','for free')
        self.dataframe['other_installments']      = self.dataframe['other_installments'        ].str.replace('A141','bank'  ).str.replace('A142','stores'      ).str.replace('A143','none')
        self.dataframe['job']                     = self.dataframe['job'                       ].str.replace('A171','no'    ).str.replace('A172','no'          ).str.replace('A173','yes'         ).str.replace('A174','yes')
        self.dataframe['telephone']               = self.dataframe['telephone'                 ].str.replace('A191','no'    ).str.replace('A192','yes')
        self.dataframe['foreign_worker']          = self.dataframe['foreign_worker'            ].str.replace('A201','yes'   ).str.replace('A202','no')
        
        if not self.tipo_procesamiento == 'reg_logistica': self.dataframe['pct_fee_income'] = self.dataframe['pct_fee_income'].astype(str).str.replace('1','low').str.replace('2','low-mid').str.replace('3','mid-high').str.replace('4','high')

    def __asegurar_encoding_numerico(self):
        """Asegura que TODAS las columnas (excepto 'target') sean numéricas.
        Si quedan strings, las transforma vía One-Hot Encoding (sin drop_first para evitar pérdida)."""
        import pandas as pd
        import numpy as np

        print("\t🔍 Verificando y saneando tipos de datos finales...")
        
        # Identificar columnas no numéricas (excluyendo 'target')
        non_numeric_cols = self.dataframe.select_dtypes(exclude=[np.number]).columns.tolist()
        if 'target' in non_numeric_cols:
            non_numeric_cols.remove('target')
        
        if non_numeric_cols:
            print(f"\t⚠️  Columnas no numéricas detectadas: {non_numeric_cols}")
            # Aplicar One-Hot Encoding *agresivo* (sin drop_first) a lo que quede
            print("\t🔧 Aplicando One-Hot Encoding final a columnas restantes...")
            try:
                # Guardar target
                target = self.dataframe['target'].copy()
                features = self.dataframe.drop(columns=['target'], errors='ignore')
                
                # One-Hot seguro (solo a object/string)
                features = pd.get_dummies(
                    features,
                    columns=non_numeric_cols,
                    dtype=int,
                    prefix=non_numeric_cols
                )
                
                # Volver a armar
                self.dataframe = pd.concat([features, target], axis=1)
                print(f"\t✅ Conversión completada. Nuevas dimensiones: {self.dataframe.shape}")
            except Exception as e:
                print(f"\t❌ Error en encoding final: {e}")
                raise
        else:
            print("\t✅ Todas las columnas (excepto target) ya son numéricas.")
    
    # ===== Logista
    def __winsorize_column(self, col):
        if col == 'month_credit_duration':
            return np.clip(self.dataframe[col], 4, 42)  # Límites del EDA
        elif col == 'credit_amount':
            return np.clip(self.dataframe[col], 250, 7882)  # Límite superior EDA
        elif col == 'age':
            return np.clip(self.dataframe[col], 19, 65)  # Considerar outliers >65

    def __crear_features_agrupadas(self,eliminar_granularidad:bool = True):
        print('\tCreando nuevas categorias agrupadas...')
        self.dataframe['fx_credit_duration'] = [('less 1 year'   if year < 12     else ('more 3 years' if year > 36     else '1 to 3 years')) for year    in self.dataframe['month_credit_duration']]
        self.dataframe['fx_credit_amount']   = [('less 3.5k'     if amount < 3500 else ('more 7k'      if amount > 7000 else '3.5k to 7k'))   for amount  in self.dataframe['credit_amount']]
        self.dataframe['fx_age']             = [('early adult'   if age < 38      else ('late adult'   if age > 57      else 'adult'))        for age     in self.dataframe['age']]

        if eliminar_granularidad: self.dataframe.drop(['month_credit_duration','credit_amount','age'],axis=1,inplace=True)

    def __aplicar_hot_encoding(self):
        print('\tAplicando One-Hot Encoding...')
        
        # 1. Guardamos la columna 'target' para que no se vea afectada por la codificación
        target = self.dataframe['target']
        features = self.dataframe.drop('target', axis=1)
        
        # 2. Aplicamos get_dummies. 
        #    - Esto convertirá automáticamente TODAS las columnas 'object' (strings) en columnas dummy.
        #    - Dejará las columnas que ya son numéricas (como 'years_of_residence') intactas.
        #    - drop_first=True es crucial para la regresión logística, ya que evita la multicolinealidad.
        #    - dtype=int asegura que las nuevas columnas sean 0 y 1, no booleanos.
        features_encoded = pd.get_dummies(features, drop_first=True, dtype=int)
        
        # 3. Volvemos a unir las features (ya 100% numéricas) con la columna target
        self.dataframe = pd.concat([features_encoded, target], axis=1)
    
    def __flujo_regresion_logistica(self):
        print('\tPreprocesamiento optimizado para regresión logística...')
        
        # 1. Tratar outliers mediante winsorización
        for col in ['credit_amount', 'month_credit_duration', 'age']:
            self.dataframe[col] = self.__winsorize_column(col)
        
        # 2. Crear variables transformadas
        self.dataframe['log_credit_amount'] = np.log1p(self.dataframe['credit_amount'])
        self.dataframe['monthly_payment'] = self.dataframe['credit_amount'] / self.dataframe['month_credit_duration']
        
        # 3. Recodificar variables categóricas
        self.__cambiar_nomenclaturas()
        
        # 4. Crear features agrupadas PERO mantener variables originales
        self.__crear_features_agrupadas(eliminar_granularidad=False)
        
        # 5. One-Hot Encoding
        self.__aplicar_hot_encoding()
        
        # 6. Estandarizar variables numéricas (aplicar después de One-Hot Encoding)
        numeric_cols = ['month_credit_duration', 'credit_amount', 'age', 'years_of_residence', 
                        'num_existing_credits', 'num_dependents', 'pct_fee_income',
                        'log_credit_amount', 'monthly_payment']
        
        scaler = StandardScaler()
        self.dataframe[numeric_cols] = scaler.fit_transform(self.dataframe[numeric_cols])

    # ===== arboles
    def __winsorize_extreme_outliers(self,col):
        Q1 = self.dataframe[col].quantile(0.25)
        Q3 = self.dataframe[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        return np.clip(self.dataframe[col], lower_bound, upper_bound)
    
    def __target_encode_purpose(self):
        global_mean = self.dataframe['target'].mean()
        purpose_counts = self.dataframe['purpose'].value_counts()
        purpose_target_means = self.dataframe.groupby('purpose')['target'].mean()

        # Regularización basada en el tamaño de cada categoría
        min_samples_leaf = 50
        smoothing = 1 / (1 + np.exp(-(purpose_counts - min_samples_leaf) / 10))
        self.dataframe['purpose_encoded'] = self.dataframe['purpose'].map(
            lambda x: smoothing[x] * purpose_target_means.get(x, global_mean) + 
                    (1 - smoothing[x]) * global_mean if x in smoothing.index else global_mean
        )

    def __flujo_arboles(self):
        print('\tPreprocesamiento optimizado para árboles de decisión...')
        
        # 1. Tratar outliers extremos (no eliminar, sino suavizar)
        for col in ['credit_amount', 'month_credit_duration']:
            self.dataframe[col] = self.__winsorize_extreme_outliers(col)
        
        # 2. Transformaciones clave basadas en EDA
        self.dataframe['credit_to_duration_ratio'] = self.dataframe['credit_amount'] / self.dataframe['month_credit_duration']
        self.dataframe['age_squared'] = self.dataframe['age'] ** 2
        
        # 3. Codificación ordinal mejorada
        ordinal_mappings = {
            'savings_type': {'A65': 0, 'A61': 1, 'A62': 2, 'A63': 3, 'A64': 4},
            'years_of_employment': {'A71': 0, 'A72': 1, 'A73': 2, 'A74': 3, 'A75': 4},
            'status_checking_account': {'A14': 0, 'A11': 1, 'A12': 2, 'A13': 3},
            'credit_history': {'A30': 0, 'A31': 1, 'A32': 2, 'A33': 3, 'A34': 4},
            'pct_fee_income': {'1': 0, '2': 1, '3': 2, '4': 3},  # Asegurar strings
            'job': {'A171': 0, 'A172': 1, 'A173': 2, 'A174': 3}
        }
        
        # 4. Creación de características basadas en hallazgos del EDA
        # Variables numéricas con alta diferencia entre clases según EDA
        self.dataframe['high_duration'] = (self.dataframe['month_credit_duration'] > 24).astype(int)
        self.dataframe['high_amount'] = (self.dataframe['credit_amount'] > 3972).astype(int)
        
        # Interacciones críticas identificadas en el EDA
        self.dataframe['high_risk_profile'] = ((self.dataframe['credit_history'].isin([0, 4])) &  # A30/A34
                                            (self.dataframe['status_checking_account'] == 1) &  # A11
                                            (self.dataframe['credit_amount'] > 3972)).astype(int)
        
        # 5. One-Hot Encoding para variables nominales
        low_cardinality_vars = ['status_sex', 'debtors', 'property', 'housing', 
                            'other_installments', 'telephone', 'foreign_worker']
        self.dataframe = pd.get_dummies(self.dataframe, columns=low_cardinality_vars, 
                                    prefix=low_cardinality_vars, dtype=int)
        
        # 6. Target Encoding regularizado para purpose
        self.__target_encode_purpose()
        
        # 7. Eliminar variables de baja relevancia según EDA
        low_relevance_vars = ['years_of_residence', 'num_dependents']
        for var in low_relevance_vars:
            if var in self.dataframe.columns:
                self.dataframe.drop(var, axis=1, inplace=True)
        
        # 8. Transformaciones adicionales para variables sesgadas
        self.dataframe['log_credit_amount'] = np.log1p(self.dataframe['credit_amount'])

    # ===== ensamble
    def __target_encoding_regularizado(self):
        global_mean = self.dataframe['target'].mean()
        min_samples_leaf = 50  # Mínimo de muestras para confiar en la media local

        # Para variables categóricas clave identificadas en el EDA
        for cat_col in ['purpose', 'status_checking_account', 'credit_history']:
            if cat_col in self.dataframe.columns:
                cat_counts = self.dataframe[cat_col].value_counts()
                cat_means = self.dataframe.groupby(cat_col)['target'].mean()
                
                # Factor de suavizado basado en el tamaño de la categoría
                smoothing = 1 / (1 + np.exp(-(cat_counts - min_samples_leaf) / 10))
                
                # Crear columna encoded
                encoded_col = f'{cat_col}_encoded'
                self.dataframe[encoded_col] = self.dataframe[cat_col].map(
                    lambda x: smoothing.get(x, 0) * cat_means.get(x, global_mean) + 
                            (1 - smoothing.get(x, 0)) * global_mean if x in cat_counts.index else global_mean
                )
                
                # Eliminar variable original después de encoding
                self.dataframe.drop(cat_col, axis=1, inplace=True)

    def __crear_interacciones_eda(self):
        """Crea interacciones usando los valores recodificados (strings)"""
        print('\tCreando interacciones específicas basadas en hallazgos del EDA...')
        
        # Combinación identificada como de máximo riesgo en el EDA
        self.dataframe['high_risk_combo'] = (
            (self.dataframe['credit_history'] == 'critical') &      # A30 - 62.5% bad loans
            (self.dataframe['status_checking_account'] == 'low') &  # A11 - 49.27% bad loans  
            (self.dataframe['credit_amount'] > 3972) &              # Monto alto (percentil 75)
            (self.dataframe['month_credit_duration'] > 24)          # Duración larga (percentil 75)
        ).astype(int)
        
        # Para el hallazgo sobre trabajadores extranjeros
        self.dataframe['domestic_worker_high_risk'] = (
            (self.dataframe['foreign_worker'] == 'no') &      # Trabajador local
            (self.dataframe['credit_history'] == 'critical')  # Historial crítico
        ).astype(int)
        
        # Interacciones de las variables más discriminativas según EDA
        self.dataframe['long_credit_high_amount'] = (
            (self.dataframe['month_credit_duration'] > 24) &  # Percentil 75
            (self.dataframe['credit_amount'] > 3972)          # Percentil 75
        ).astype(int)
        
        self.dataframe['critical_history_low_balance'] = (
            (self.dataframe['credit_history'].isin(['critical', 'warning'])) &  # A30/A34
            (self.dataframe['status_checking_account'] == 'low')                # A11
        ).astype(int)

    def __crear_variables_riesgo_acumulativo(self):
        """Crea variables de riesgo usando los valores recodificados"""
        print('\tCreando variables de riesgo acumulativo...')
        
        # Variable acumulativa de factores de riesgo identificados en el EDA
        risk_factors = [
            # Factores con >25% diferencia entre clases según EDA
            (self.dataframe['credit_amount'] > 3972).astype(int),
            (self.dataframe['month_credit_duration'] > 24).astype(int),
            (self.dataframe['credit_history'].isin(['critical', 'warning'])).astype(int),
            (self.dataframe['status_checking_account'] == 'low').astype(int),
            # Factores con 15-25% diferencia
            (self.dataframe['savings_type'] == 'low').astype(int),
            (self.dataframe['years_of_employment'] == 'jr').astype(int),
            (self.dataframe['purpose'].isin(['durable-goods'])).astype(int),
            (self.dataframe['debtors'] == 'co-applicant').astype(int),
            (self.dataframe['housing'] == 'rent').astype(int),
            (self.dataframe['other_installments'].isin(['bank', 'stores'])).astype(int)
        ]
        
        self.dataframe['risk_factor_count'] = sum(risk_factors)
        self.dataframe['risk_factor_ratio'] = self.dataframe['risk_factor_count'] / len(risk_factors)
        
        # Score de estabilidad financiera (inverso al riesgo)
        stability_factors = [
            (self.dataframe['credit_history'] == 'good').astype(int),
            (self.dataframe['status_checking_account'] == 'high').astype(int),
            (self.dataframe['savings_type'] == 'high').astype(int),
            (self.dataframe['years_of_employment'] == 'sr').astype(int),
            (self.dataframe['property'].isin(['high', 'mid'])).astype(int),
            (self.dataframe['housing'] == 'own').astype(int),
            (self.dataframe['foreign_worker'] == 'yes').astype(int),
            (self.dataframe['age'] >= 38).astype(int)
        ]
        
        self.dataframe['stability_factor_count'] = sum(stability_factors)
        self.dataframe['stability_factor_ratio'] = self.dataframe['stability_factor_count'] / len(stability_factors)

    def __eliminar_variables_baja_relevancia(self):
        print('\tEliminando variables de baja relevancia según EDA bivariado...')
        
        # Variables con mínima diferencia entre clases según EDA bivariado (<1%)
        low_relevance_vars = [
            'years_of_residence',    # 0.25% diferencia
            'num_dependents'         # 0.21% diferencia
        ]
        
        # Variables con diferencia moderada pero que pueden ser redundantes
        moderate_relevance_vars = [
            'num_existing_credits',  # 4.05% diferencia
            'age'                    # 6.24% diferencia
        ]
        
        # Eliminar variables de muy baja relevancia
        for var in low_relevance_vars:
            if var in self.dataframe.columns:
                print(f"\t\tEliminando variable de muy baja relevancia: {var}")
                self.dataframe.drop(var, axis=1, inplace=True)
        
        # Considerar eliminar variables de relevancia moderada si ya tenemos transformaciones
        for var in moderate_relevance_vars:
            if var in self.dataframe.columns:
                print(f"\t\tConsiderando eliminación de variable de relevancia moderada: {var}")
                # Mantener si no tenemos transformaciones alternativas
                if f'log_{var}' not in self.dataframe.columns and f'{var}_binned' not in self.dataframe.columns:
                    print(f"\t\tManteniendo {var} por no tener transformaciones alternativas")
                else:
                    print(f"\t\tEliminando {var} por tener transformaciones alternativas")
                    self.dataframe.drop(var, axis=1, inplace=True)

    def __aplicar_one_hot_encoding_selectivo(self):
        print('\tAplicando One-Hot Encoding selectivo a variables nominales restantes...')
        
        # Identificar variables categóricas restantes (object o category dtype)
        categorical_cols = self.dataframe.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Excluir variables que ya fueron codificadas o que serán eliminadas
        cols_to_exclude = ['purpose']  # Ya fue target encoded
        
        for col in cols_to_exclude:
            if col in categorical_cols:
                categorical_cols.remove(col)
        
        # Aplicar One-Hot Encoding selectivo
        if categorical_cols:
            print(f"\t\tAplicando One-Hot Encoding a: {categorical_cols}")
            self.dataframe = pd.get_dummies(
                self.dataframe, 
                columns=categorical_cols, 
                prefix=categorical_cols,
                dtype=int,
                drop_first=True  # Evitar multicolinealidad
            )
        else:
            print("\t\tNo hay variables categóricas restantes para codificar")

    def __feature_selection(self):
        print('\tRealizando feature selection final basado en varianza y correlación...')
    
        # 1. Eliminar variables con varianza muy baja (<1%)
        numeric_cols = self.dataframe.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        low_variance_cols = []
        for col in numeric_cols:
            variance = self.dataframe[col].var()
            if variance < 0.01:  # Umbral de varianza
                low_variance_cols.append(col)
                print(f"\t\tVariable de baja varianza detectada: {col} (var={variance:.4f})")
        
        # Eliminar las columnas de baja varianza
        for col in low_variance_cols:
            if col in self.dataframe.columns:
                self.dataframe.drop(col, axis=1, inplace=True)
        
        # ACTUALIZAR: Recalcular numeric_cols después de eliminar las de baja varianza
        numeric_cols = self.dataframe.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        # 2. Eliminar variables altamente correlacionadas (>0.9)
        if len(numeric_cols) > 0:  # Solo proceder si hay columnas numéricas restantes
            corr_matrix = self.dataframe[numeric_cols].corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            
            high_corr_cols = []
            for col in upper.columns:
                high_corr = upper.index[upper[col] > 0.9].tolist()
                for high_corr_col in high_corr:
                    if f"{col}_{high_corr_col}" not in [f"{a}_{b}" for a, b in high_corr_cols]:
                        high_corr_cols.append((col, high_corr_col))
                        print(f"\t\tVariables altamente correlacionadas: {col} y {high_corr_col} (corr={upper[col][high_corr_col]:.4f})")
            
            # Mantener la variable con mayor correlación con el target
            cols_to_drop = []
            for col1, col2 in high_corr_cols:
                if col1 in self.dataframe.columns and col2 in self.dataframe.columns:
                    corr1 = abs(self.dataframe[col1].corr(self.dataframe['target']))
                    corr2 = abs(self.dataframe[col2].corr(self.dataframe['target']))
                    
                    if corr1 < corr2:
                        cols_to_drop.append(col1)
                    else:
                        cols_to_drop.append(col2)
            
            for col in set(cols_to_drop):
                if col in self.dataframe.columns:
                    print(f"\t\tEliminando variable redundante: {col}")
                    self.dataframe.drop(col, axis=1, inplace=True)
        else:
            print("\t\tNo hay variables numéricas restantes para analizar correlación")

    def __flujo_ensamble(self):
        print('\tPreprocesamiento optimizado para modelos ensemble...')
        
        # 1. Recodificar variables categóricas primero
        self.__cambiar_nomenclaturas()
        
        # 2. Crear interacciones específicas basadas en hallazgos del EDA
        self.__crear_interacciones_eda()
        
        # 3. Crear variables de riesgo acumulativo
        self.__crear_variables_riesgo_acumulativo()
        
        # 4. Tratar outliers extremos (no eliminar, sino suavizar)
        for col in ['credit_amount', 'month_credit_duration', 'num_dependents']:
            if col in self.dataframe.columns:
                self.dataframe[col] = self.__winsorize_extreme_outliers(col)
        
        # 5. Mantener transformaciones logarítmicas valiosas
        self.dataframe['log_credit_amount'] = np.log1p(self.dataframe['credit_amount'])
        self.dataframe['log_credit_duration'] = np.log1p(self.dataframe['month_credit_duration'])
        
        # 6. Target encoding regularizado para variables categóricas clave
        self.__target_encoding_regularizado()
        
        # 7. Eliminar variables de baja relevancia según EDA bivariado
        self.__eliminar_variables_baja_relevancia()
        
        # 8. One-Hot Encoding para variables nominales restantes
        self.__aplicar_one_hot_encoding_selectivo()
        
        # 9. Feature selection final basado en varianza y correlación
        self.__feature_selection()
        
        # 10. Crear variables adicionales para ensemble
        print('\tCreando variables adicionales para ensemble...')
        
        # Interacciones específicas para ensembles
        if 'status_checking_account_encoded' in self.dataframe.columns and 'credit_history_encoded' in self.dataframe.columns:
            self.dataframe['checking_credit_interaction'] = (
                self.dataframe['status_checking_account_encoded'] * 
                self.dataframe['credit_history_encoded']
            )
        
        if 'years_of_employment_encoded' in self.dataframe.columns and 'savings_type_encoded' in self.dataframe.columns:
            self.dataframe['employment_savings_interaction'] = (
                self.dataframe['years_of_employment_encoded'] * 
                self.dataframe['savings_type_encoded']
            )
        
        if 'age' in self.dataframe.columns and 'credit_to_duration_ratio' in self.dataframe.columns:
            self.dataframe['age_credit_ratio'] = self.dataframe['age'] / (self.dataframe['credit_to_duration_ratio'] + 1)
        
        # Binning estratégico para variables continuas
        if 'age' in self.dataframe.columns:
            self.dataframe['age_binned'] = pd.cut(
                self.dataframe['age'], 
                bins=[0, 25, 35, 45, 55, 100], 
                labels=[0, 1, 2, 3, 4],
                include_lowest=True
            ).astype(int)
        
        if 'credit_amount' in self.dataframe.columns:
            self.dataframe['credit_amount_binned'] = pd.cut(
                self.dataframe['credit_amount'],
                bins=[0, 2500, 5000, 7500, 10000, 20000],
                labels=[0, 1, 2, 3, 4],
                include_lowest=True
            ).astype(int)
        
        # CORRECCIÓN: Usar las columnas dummy de pct_fee_income en lugar de la columna original
        # Ratios y proporciones - debt_burden
        pct_fee_dummy_cols = [col for col in self.dataframe.columns if col.startswith('pct_fee_income_')]
        if pct_fee_dummy_cols and 'credit_amount' in self.dataframe.columns:
            # Calcular debt_burden usando la categoría con mayor riesgo (pct_fee_income_high)
            if 'pct_fee_income_high' in self.dataframe.columns:
                self.dataframe['debt_burden'] = self.dataframe['credit_amount'] / (
                    self.dataframe['pct_fee_income_high'] + 1
                )
            else:
                # Si no existe 'high', usar la primera disponible
                self.dataframe['debt_burden'] = self.dataframe['credit_amount'] / (
                    self.dataframe[pct_fee_dummy_cols[0]] + 1
                )
        
        # CORRECCIÓN: stability_score - verificar que las columnas existan
        if ('years_of_residence' in self.dataframe.columns and 
            'years_of_employment_encoded' in self.dataframe.columns and 
            'age' in self.dataframe.columns):
            self.dataframe['stability_score'] = (
                self.dataframe['years_of_residence'] + 
                self.dataframe['years_of_employment_encoded']
            ) / (self.dataframe['age'] + 1)
        else:
            print("\t\tNo se pudo crear 'stability_score' - faltan columnas requeridas")

    # ===== Red Neuronal
    def __winsorize_outliers_neural(self, col):
        """Suaviza outliers manteniendo información extrema pero reduciendo su impacto"""
        Q1 = self.dataframe[col].quantile(0.25)
        Q3 = self.dataframe[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 2.5 * IQR  # Límite más conservador que para árboles
        upper_bound = Q3 + 2.5 * IQR
        return np.clip(self.dataframe[col], lower_bound, upper_bound)

    def __create_polynomial_features(self):
        """Crea características polinómicas para capturar relaciones no lineales"""
        print('\tCreando características polinómicas para relaciones no lineales...')
        
        # Transformación logarítmica para variables sesgadas
        self.dataframe['log_credit_amount'] = np.log1p(self.dataframe['credit_amount'])
        self.dataframe['log_month_credit_duration'] = np.log1p(self.dataframe['month_credit_duration'])
        
        # Características polinómicas para variables clave según EDA
        self.dataframe['credit_amount_sq'] = self.dataframe['credit_amount'] ** 2
        self.dataframe['credit_duration_sq'] = self.dataframe['month_credit_duration'] ** 2
        self.dataframe['age_sq'] = self.dataframe['age'] ** 2
        
        # Interacciones de segundo orden para variables con alta correlación con target
        self.dataframe['credit_duration_amount_ratio'] = (
            self.dataframe['credit_amount'] / (self.dataframe['month_credit_duration'] + 1)
        )
        self.dataframe['age_credit_ratio'] = self.dataframe['age'] / (self.dataframe['credit_amount'] + 1)
        
        # Características cíclicas para edad (capturar efectos no lineales)
        self.dataframe['age_sin'] = np.sin(2 * np.pi * self.dataframe['age'] / 100)
        self.dataframe['age_cos'] = np.cos(2 * np.pi * self.dataframe['age'] / 100)

    def __categorize_features_for_embedding(self):
        """Prepara variables categóricas para embeddings en la red neuronal"""
        print('\tPreparando variables categóricas para embeddings...')
        
        # Mapeo de variables categóricas a enteros para embeddings
        categorical_vars = [
            'status_checking_account', 'credit_history', 'purpose', 'savings_type',
            'years_of_employment', 'status_sex', 'debtors', 'property',
            'other_installments', 'housing', 'job', 'telephone', 'foreign_worker'
        ]
        
        for var in categorical_vars:
            if var in self.dataframe.columns:
                # Crear mapeo de categorías a enteros
                categories = sorted(self.dataframe[var].unique())
                cat_to_idx = {cat: idx for idx, cat in enumerate(categories)}
                self.dataframe[f'{var}_idx'] = self.dataframe[var].map(cat_to_idx)
        
        # Eliminar variables originales después de crear los índices
        self.dataframe.drop(categorical_vars, axis=1, inplace=True)

    def __normalize_features(self):
        """Normaliza todas las características numéricas al rango [0,1]"""
        print('\tNormalizando características para la red neuronal...')
        
        # Identificar todas las columnas numéricas excepto target
        numeric_cols = self.dataframe.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols.remove('target')
        
        # Normalización Min-Max para todas las características numéricas
        for col in numeric_cols:
            min_val = self.dataframe[col].min()
            max_val = self.dataframe[col].max()
            if max_val != min_val:  # Evitar división por cero
                self.dataframe[col] = (self.dataframe[col] - min_val) / (max_val - min_val)
            else:
                # Si todos los valores son iguales, establecer a 0.5
                self.dataframe[col] = 0.5
        
        # Asegurar que no haya NaN después de la normalización
        self.dataframe[numeric_cols] = self.dataframe[numeric_cols].fillna(0.5)

    def __create_risk_profiles(self):
        """Crea variables sintéticas que representen perfiles de riesgo identificados en el EDA"""
        print('\tCreando perfiles de riesgo sintéticos...')
        
        # Perfil de alto riesgo según EDA (más de 50% de préstamos malos)
        self.dataframe['high_risk_profile'] = (
            (self.dataframe['credit_history'] == 'critical') |  # A30 - 62.5% bad loans
            ((self.dataframe['status_checking_account'] == 'low') &  # A11 - 49.27% bad loans
            (self.dataframe['credit_amount'] > 3972)) |
            ((self.dataframe['purpose'] == 'durable-goods') &
            (self.dataframe['month_credit_duration'] > 24))
        ).astype(int)
        
        # Perfil de bajo riesgo según EDA (menos de 20% de préstamos malos)
        self.dataframe['low_risk_profile'] = (
            (self.dataframe['credit_history'] == 'good') &  # A31/A32 - ~30% bad loans (mejor que promedio)
            (self.dataframe['status_checking_account'] == 'high') &  # A13 - 22.22% bad loans
            (self.dataframe['savings_type'] == 'high') &
            (self.dataframe['years_of_employment'] == 'sr')
        ).astype(int)
        
        # Tendencia de riesgo acumulativo
        risk_factors = [
            (self.dataframe['credit_history'] == 'critical').astype(int),
            (self.dataframe['credit_history'] == 'warning').astype(int),
            (self.dataframe['status_checking_account'] == 'low').astype(int),
            (self.dataframe['savings_type'] == 'low').astype(int),
            (self.dataframe['years_of_employment'] == 'jr').astype(int),
            (self.dataframe['credit_amount'] > 3972).astype(int),
            (self.dataframe['month_credit_duration'] > 24).astype(int),
            (self.dataframe['debtors'] == 'co-applicant').astype(int),
            (self.dataframe['housing'] == 'rent').astype(int)
        ]
        
        self.dataframe['cumulative_risk_score'] = sum(risk_factors) / len(risk_factors)

    def __flujo_neuronal(self):
        print('\tPreprocesamiento optimizado para red neuronal...')
        
        # 1. Recodificar variables categóricas primero para mantener consistencia
        self.__cambiar_nomenclaturas()
        
        # 2. Suavizar outliers extremos (menos agresivo que para otros modelos)
        for col in ['credit_amount', 'month_credit_duration', 'age', 'num_dependents']:
            if col in self.dataframe.columns:
                self.dataframe[col] = self.__winsorize_outliers_neural(col)
        
        # 3. Crear características no lineales y polinómicas
        self.__create_polynomial_features()
        
        # 4. Crear perfiles de riesgo sintéticos basados en hallazgos del EDA
        self.__create_risk_profiles()
        
        # 5. Preparar variables categóricas para embeddings
        self.__categorize_features_for_embedding()
        
        # 6. Eliminar variables de muy baja relevancia según EDA bivariado
        low_relevance_vars = ['years_of_residence', 'num_dependents']
        for var in low_relevance_vars:
            if var in self.dataframe.columns:
                print(f"\t\tEliminando variable de muy baja relevancia: {var}")
                self.dataframe.drop(var, axis=1, inplace=True)
        
        # 7. Normalizar todas las características numéricas al rango [0,1]
        self.__normalize_features()
        
        # 8. Crear características adicionales específicas para redes neuronales
        
        # Características de interacción para capturar dependencias complejas
        if 'credit_amount' in self.dataframe.columns and 'month_credit_duration' in self.dataframe.columns:
            self.dataframe['credit_duration_interaction'] = (
                self.dataframe['credit_amount'] * self.dataframe['month_credit_duration']
            )
        
        if 'age' in self.dataframe.columns and 'credit_history_idx' in self.dataframe.columns:
            self.dataframe['age_history_interaction'] = (
                self.dataframe['age'] * self.dataframe['credit_history_idx']
            )
        
        # Característica de estabilidad financiera
        financial_stability_factors = [
            'status_checking_account_idx', 'savings_type_idx', 
            'years_of_employment_idx', 'property_idx'
        ]
        available_factors = [f for f in financial_stability_factors if f in self.dataframe.columns]
        
        if available_factors:
            self.dataframe['financial_stability_index'] = self.dataframe[available_factors].mean(axis=1)
        
        # Características de agrupamiento para edad y monto
        # (esto ayuda a la red a aprender patrones por segmentos)
        self.dataframe['age_group'] = pd.cut(
            self.dataframe['age'],
            bins=[0, 25, 35, 45, 55, 100],
            labels=[0.2, 0.4, 0.6, 0.8, 1.0],
            include_lowest=True
        ).astype(float)
        
        self.dataframe['amount_group'] = pd.cut(
            self.dataframe['credit_amount'],
            bins=[0, 1365, 2319, 3972, 10000, 20000],
            labels=[0.2, 0.4, 0.6, 0.8, 1.0],
            include_lowest=True
        ).astype(float)
        
        # 9. Normalizar nuevamente todas las características después de crear las nuevas
        self.__normalize_features()
        
        print('\tPreprocesamiento para red neuronal completado. Todas las características están en el rango [0,1].')


    # =============== METODOS PUBLICOS ===============
    def process(self):
        if not self.tipo_procesamiento in ['reg_logistica','arboles','ensamble','red_neuronal']: raise Exception(f"La opción '{self.tipo_procesamiento}' no esta permitida. Solo se permite ['reg_logistica','arboles','ensamble','red_neuronal'].")
        print(f"{'='*15} Iniciando procesamiento {self.tipo_procesamiento} {'='*15}")


        self.__cargar_dataframe()
        self.__validar_tipos_de_dato()

        if self.tipo_procesamiento   == 'reg_logistica': self.__flujo_regresion_logistica()
        elif self.tipo_procesamiento == 'arboles':       self.__flujo_arboles()
        elif self.tipo_procesamiento == 'ensamble':      self.__flujo_ensamble()
        elif self.tipo_procesamiento == 'red_neuronal':  self.__flujo_neuronal()

        self.__asegurar_encoding_numerico()
        self.__explicar_dataframe()
        self.__guardar_dataframe()




preprocesador = PreprocesarData(
    tipo_procesamiento = args.tipoProcesamiento
)
preprocesador.process()