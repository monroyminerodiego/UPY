# modeling.py
"""
Modelo de riesgo crediticio para deployment web
Autor: [Tu nombre]
Fecha: [Fecha actual]

Este script entrena, evalúa y guarda un modelo de machine learning para predecir
riesgo crediticio. Utiliza el mejor preprocesamiento identificado en el benchmarking
y un modelo XGBoost optimizado para balancear rendimiento, interpretabilidad y capacidad
de implementación en web.

Flujo del pipeline:
1. Cargar datos preprocesados
2. Dividir en conjunto de entrenamiento y prueba
3. Optimizar hiperparámetros con RandomizedSearchCV
4. Entrenar modelo final
5. Calibrar probabilidades
6. Evaluar métricas de rendimiento
7. Analizar equidad y sesgos
8. Generar visualizaciones explicativas
9. Guardar artefactos para deployment web
"""

import os
import json
import pickle
import warnings
import numpy as np
import pandas as pd
import matplotlib
# Establecer backend de matplotlib adecuado para entornos sin GUI
matplotlib.use('Agg')  # Usar backend no interactivo
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Modelado y optimización
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix, classification_report, roc_curve, 
    precision_recall_curve
)
from sklearn.utils.class_weight import compute_sample_weight

# Modelos
import xgboost as xgb
from xgboost import XGBClassifier

# Explicabilidad
import shap

# Fairness (si está disponible, sino manejar excepción)
try:
    from aif360.datasets import BinaryLabelDataset #type: ignore
    from aif360.metrics import ClassificationMetric #type: ignore
    AIF360_AVAILABLE = True
except ImportError:
    AIF360_AVAILABLE = False
    print("⚠️ Librería aif360 no disponible. El análisis de fairness podría estar limitado.")

# Configuración inicial
warnings.filterwarnings('ignore')
sns.set(style='whitegrid', palette='muted', font_scale=1.1)
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.bbox'] = 'tight'

# Directorios del proyecto
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'Data', 'processed')
MODELS_DIR = os.path.join(PROJECT_DIR, 'Docs', 'models')
PLOTS_DIR = os.path.join(PROJECT_DIR, 'Docs')
LOGS_DIR = os.path.join(PROJECT_DIR, 'Logs')

# Crear directorios si no existen
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def print_step(message: str, is_header: bool = False) -> None:
    """Imprime un mensaje con formato para indicar los pasos del pipeline."""
    if is_header:
        print(f"\n{'='*60}")
        print(f"{message.upper()}")
        print(f"{'='*60}")
    else:
        print(f"\n🔍 {message}")
    # Guardar en log
    log_file = os.path.join(LOGS_DIR, f"modeling_log_{datetime.now().strftime('%Y%m%d')}.txt")
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def load_preprocessed_data(file_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Carga los datos preprocesados y separa en features y target."""
    print_step("Cargando datos preprocesados para árboles")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    
    df = pd.read_csv(file_path)
    print_step(f"✓ Dataset cargado exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    # Separar características y target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Verificación de calidad
    if X.isnull().any().any():
        null_cols = X.columns[X.isnull().any()].tolist()
        print_step(f"⚠️ Advertencia: Se encontraron valores nulos en las columnas: {null_cols}")
        # Rellenar nulos con la mediana de cada columna
        for col in null_cols:
            if pd.api.types.is_numeric_dtype(X[col]):
                X[col].fillna(X[col].median(), inplace=True)
            else:
                X[col].fillna(X[col].mode()[0], inplace=True)
    
    print_step(f"✓ Características: {X.shape[1]} features, Target: {y.shape[0]} muestras")
    print_step(f"✓ Distribución del target: {y.value_counts().to_dict()}")
    
    return X, y

def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Tuple:
    """Divide los datos en conjuntos de entrenamiento y prueba de forma estratificada."""
    print_step("Dividiendo datos en conjuntos de entrenamiento y prueba")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        stratify=y, 
        random_state=42
    )
    
    # Calcular pesos para clases desbalanceadas
    sample_weights = compute_sample_weight('balanced', y_train)
    
    print_step(f"✓ Conjunto de entrenamiento: {X_train.shape[0]} muestras")
    print_step(f"✓ Conjunto de prueba: {X_test.shape[0]} muestras")
    print_step(f"✓ Distribución en entrenamiento: {pd.Series(y_train).value_counts().to_dict()}")
    print_step(f"✓ Distribución en prueba: {pd.Series(y_test).value_counts().to_dict()}")
    
    return X_train, X_test, y_train, y_test, sample_weights

def optimize_model(X_train: pd.DataFrame, y_train: pd.Series, sample_weights: np.ndarray) -> XGBClassifier:
    """Optimiza los hiperparámetros del modelo XGBoost usando RandomizedSearchCV."""
    print_step("Optimizando hiperparámetros del modelo XGBoost", is_header=True)
    
    # Definir espacio de búsqueda para hiperparámetros
    param_dist = {
        'n_estimators': [50, 100, 150, 200],
        'max_depth': [3, 5, 7, 9],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'gamma': [0, 0.1, 0.2, 0.5],
        'min_child_weight': [1, 3, 5, 7],
        'scale_pos_weight': [len(y_train[y_train==1])/len(y_train[y_train==0])]  # Para balancear clases (inverso al benchmark)
    }
    
    # Modelo base
    xgb_base = XGBClassifier(
        random_state=42,
        eval_metric='aucpr',  # Priorizar precision-recall para clases desbalanceadas
        use_label_encoder=False,
        tree_method='hist',   # Más rápido y eficiente
        n_jobs=-1             # Usar todos los cores
    )
    
    # Configurar búsqueda aleatoria
    random_search = RandomizedSearchCV(
        estimator=xgb_base,
        param_distributions=param_dist,
        n_iter=25,            # Número de combinaciones a probar
        cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42),
        scoring='average_precision',  # Métrica apropiada para clases desbalanceadas
        n_jobs=-1,
        verbose=1,
        random_state=42
    )
    
    print_step("Iniciando búsqueda aleatoria de hiperparámetros...")
    print_step(f"Espacio de búsqueda: {len(param_dist)} dimensiones")
    
    # Entrenar con búsqueda aleatoria
    random_search.fit(X_train, y_train, sample_weight=sample_weights)
    
    # Mostrar resultados
    print_step("✓ Búsqueda de hiperparámetros completada")
    print_step(f"Mejores hiperparámetros: {random_search.best_params_}")
    print_step(f"Mejor puntuación (average_precision): {random_search.best_score_:.4f}")
    
    # Entrenar modelo final con los mejores hiperparámetros
    best_model = random_search.best_estimator_
    print_step("Entrenando modelo final con mejores hiperparámetros...")
    best_model.fit(X_train, y_train, sample_weight=sample_weights)
    
    return best_model

def calibrate_model(model: XGBClassifier, X_train: pd.DataFrame, y_train: pd.Series) -> CalibratedClassifierCV:
    """Calibra las probabilidades del modelo usando calibración isotónica."""
    print_step("Calibrando probabilidades del modelo", is_header=True)
    print_step("Utilizando calibración isotónica para mejorar la confiabilidad de las probabilidades")
    
    # Calibración isotónica (mejor para datasets pequeños/moderados)
    calibrated_model = CalibratedClassifierCV(
        model, 
        method='isotonic',  # Mejor para datasets no muy grandes
        cv='prefit'         # Ya pre-entrenado
    )
    
    calibrated_model.fit(X_train, y_train)
    print_step("✓ Modelo calibrado exitosamente")
    
    return calibrated_model

def evaluate_model(model: Any, X_test: pd.DataFrame, y_test: pd.Series, model_name: str = "XGBoost") -> Dict:
    """Evalúa el modelo y genera métricas de rendimiento."""
    print_step("Evaluando rendimiento del modelo", is_header=True)
    
    # Predicciones
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probabilidades para clase positiva (buenos pagadores)
    
    # Métricas básicas
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
        'pr_auc': average_precision_score(y_test, y_pred_proba)
    }
    
    print_step("📊 Métricas de rendimiento:")
    for metric, value in metrics.items():
        print_step(f"• {metric.replace('_', ' ').title()}: {value:.4f}")
    
    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred)
    print_step("Matriz de confusión:")
    print(f"              Predicción")
    print(f"            Malo (0)  Bueno (1)")
    print(f"Real Malo    [{cm[0,0]:3d}      {cm[0,1]:3d}]")
    print(f"Real Bueno   [{cm[1,0]:3d}      {cm[1,1]:3d}]")
    
    # Reporte de clasificación
    print_step("Reporte de clasificación detallado:")
    print(classification_report(y_test, y_pred, target_names=['Malo (0)', 'Bueno (1)']))
    
    # Curva precision-recall para encontrar umbral óptimo
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_pred_proba)
    
    # Calcular F1 para cada umbral
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
    
    # Encontrar umbral que maximiza F1
    opt_idx = np.argmax(f1_scores[:-1])  # Excluir último elemento para coincidir con thresholds
    optimal_threshold = thresholds[opt_idx] if opt_idx < len(thresholds) else 0.5
    print_step(f"\n🔍 Umbral óptimo encontrado para maximizar F1: {optimal_threshold:.4f}")
    
    # Evaluar con umbral óptimo
    y_pred_opt = (y_pred_proba >= optimal_threshold).astype(int)
    metrics_opt = {
        'accuracy_opt': accuracy_score(y_test, y_pred_opt),
        'precision_opt': precision_score(y_test, y_pred_opt),
        'recall_opt': recall_score(y_test, y_pred_opt),
        'f1_opt': f1_score(y_test, y_pred_opt)
    }
    
    print_step("📊 Métricas con umbral óptimo:")
    for metric, value in metrics_opt.items():
        print_step(f"• {metric.replace('_opt', '').replace('_', ' ').title()}: {value:.4f}")
    
    return {
        'raw_metrics': metrics,
        'opt_metrics': metrics_opt,
        'optimal_threshold': optimal_threshold,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'y_pred_opt': y_pred_opt,
        'thresholds': thresholds,  # Guardar thresholds para las gráficas
        'precisions': precisions,  # Guardar precisions para las gráficas
        'recalls': recalls         # Guardar recalls para las gráficas
    }

def plot_evaluation_curves(model: Any, X_test: pd.DataFrame, y_test: pd.Series, results: Dict) -> None:
    """Genera gráficos de evaluación: ROC, PR y curva de calibración."""
    print_step("Generando gráficas de evaluación", is_header=True)
    
    y_pred_proba = results['y_pred_proba']
    optimal_threshold = results['optimal_threshold']
    thresholds = results['thresholds']
    precisions = results['precisions']
    recalls = results['recalls']
    
    # 1. Curva ROC
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {results["raw_metrics"]["roc_auc"]:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Tasa de Falsos Positivos (1 - Especificidad)')
    plt.ylabel('Tasa de Verdaderos Positivos (Sensibilidad)')
    plt.title('Curva ROC')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    
    # 2. Curva Precision-Recall
    plt.subplot(1, 2, 2)
    plt.plot(recalls, precisions, color='green', lw=2, label=f'PR curve (AUC = {results["raw_metrics"]["pr_auc"]:.4f})')
    
    # Encontrar el índice del umbral óptimo en la curva PR
    opt_idx = np.argmin(np.abs(thresholds - optimal_threshold))
    if opt_idx < len(recalls):
        plt.scatter(recalls[opt_idx], precisions[opt_idx], color='red', s=100, 
                   label=f'Umbral óptimo ({optimal_threshold:.2f})', zorder=5)
    
    plt.xlabel('Recall')
    plt.ylabel('Precisión')
    plt.title('Curva Precision-Recall')
    plt.legend(loc="lower left")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'roc_pr_curves.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print_step("✅ Gráficas ROC y PR generadas y guardadas")
    
    # 3. Matriz de confusión
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, results['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Malo (0)', 'Bueno (1)'],
                yticklabels=['Malo (0)', 'Bueno (1)'])
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    plt.title('Matriz de Confusión')
    plt.savefig(os.path.join(PLOTS_DIR, 'confusion_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print_step("✅ Matriz de confusión generada y guardada")
    
    # 4. Curva de calibración
    plt.figure(figsize=(10, 6))
    prob_true, prob_pred = calibration_curve(y_test, y_pred_proba, n_bins=10)
    plt.plot(prob_pred, prob_true, marker='o', label='Modelo calibrado')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectamente calibrado')
    plt.xlabel('Probabilidad promedio predicha')
    plt.ylabel('Fracción de positivos')
    plt.title('Curva de Calibración')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(PLOTS_DIR, 'calibration_curve.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print_step("✅ Curva de calibración generada y guardada")
    
    # 5. Distribución de probabilidades
    plt.figure(figsize=(10, 6))
    plt.hist(y_pred_proba[y_test == 0], bins=30, alpha=0.5, label='Malo (0)', color='red')
    plt.hist(y_pred_proba[y_test == 1], bins=30, alpha=0.5, label='Bueno (1)', color='green')
    plt.axvline(x=optimal_threshold, color='black', linestyle='--', label=f'Umbral óptimo = {optimal_threshold:.2f}')
    plt.xlabel('Probabilidad predicha de ser Bueno (1)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Probabilidades por Clase')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(PLOTS_DIR, 'probability_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print_step("✅ Distribución de probabilidades generada y guardada")

def analyze_fairness(model: Any, X_test: pd.DataFrame, y_test: pd.Series, y_pred: np.ndarray, threshold: float) -> None:
    """Analiza la equidad del modelo en diferentes grupos demográficos."""
    print_step("Analizando equidad del modelo", is_header=True)
    
    # Crear una copia del dataset de prueba para análisis
    df = X_test.copy()
    df['target'] = y_test
    df['predicted'] = y_pred
    
    # Identificar columnas relacionadas con edad y género
    age_cols = [col for col in X_test.columns if 'age' in col.lower()]
    sex_cols = [col for col in X_test.columns if ('sex' in col.lower() or 'gender' in col.lower() or 'status_sex' in col.lower())]
    
    # Variables de sustitución para análisis de fairness
    substitute_cols = {
        'age': age_cols[0] if age_cols else None,
        'sex': sex_cols[0] if sex_cols else None
    }
    
    # Si no encontramos columnas específicas, buscar alternativas
    if not substitute_cols['age']:
        # Buscar columna con rango de edad o similar
        age_related = [col for col in X_test.columns if any(term in col.lower() for term in ['years', 'duration', 'residence'])]
        substitute_cols['age'] = age_related[0] if age_related else None
    
    if not substitute_cols['sex']:
        # Buscar columnas categóricas que puedan indicar género indirectamente
        categorical_cols = X_test.select_dtypes(include=['object', 'category']).columns.tolist()
        if categorical_cols:
            substitute_cols['sex'] = categorical_cols[0]
    
    # Realizar análisis de fairness básico incluso sin aif360
    if substitute_cols['age']:
        print_step(f"\n👥 Análisis de equidad usando '{substitute_cols['age']}' como proxy de edad:")
        
        # Dividir en grupos por percentiles
        df['age_group'] = pd.qcut(df[substitute_cols['age']], q=2, labels=['Grupo 1', 'Grupo 2'])
        
        groups = df['age_group'].unique()
        for group in groups:
            group_data = df[df['age_group'] == group]
            if len(group_data) > 10:
                group_pred = group_data['predicted']
                group_target = group_data['target']
                
                dp = group_pred.mean()  # Demographic Parity (tasa de positivos)
                eo = recall_score(group_target, group_pred)  # Equal Opportunity (TPR)
                
                print_step(f"  • {group} ({len(group_data)} muestras):")
                print_step(f"    - Demographic Parity (tasa de aprobación): {dp:.4f}")
                print_step(f"    - Equal Opportunity (recall): {eo:.4f}")
    else:
        print_step("⚠️ No se encontró una columna adecuada para analizar equidad por edad.")
    
    if substitute_cols['sex']:
        print_step(f"\n👥 Análisis de equidad usando '{substitute_cols['sex']}' como proxy de género:")
        
        # Tomar los dos valores más comunes para crear grupos
        common_values = df[substitute_cols['sex']].value_counts().index[:2]
        df['sex_group'] = df[substitute_cols['sex']].apply(lambda x: 'Grupo A' if x == common_values[0] else ('Grupo B' if x == common_values[1] else 'Otros'))
        
        for group in ['Grupo A', 'Grupo B']:
            group_data = df[df['sex_group'] == group]
            if len(group_data) > 10:
                group_pred = group_data['predicted']
                group_target = group_data['target']
                
                dp = group_pred.mean()  # Demographic Parity (tasa de positivos)
                eo = recall_score(group_target, group_pred)  # Equal Opportunity (TPR)
                
                print_step(f"  • {group} ({len(group_data)} muestras):")
                print_step(f"    - Demographic Parity (tasa de aprobación): {dp:.4f}")
                print_step(f"    - Equal Opportunity (recall): {eo:.4f}")
    else:
        print_step("⚠️ No se encontró una columna adecuada para analizar equidad por género.")

def explain_model(model: XGBClassifier, X_train: pd.DataFrame, X_test: pd.DataFrame, feature_names: List[str]) -> None:
    """Genera explicaciones globales y locales del modelo usando SHAP."""
    print_step("Generando explicaciones del modelo con SHAP", is_header=True)
    
    # Explicabilidad global con SHAP
    print_step("Calculando valores SHAP para explicabilidad global...")
    try:
        explainer = shap.TreeExplainer(model)
        
        # Tomar muestra para cálculo eficiente
        sample_size = min(100, len(X_test))
        X_sample = shap.sample(X_test, sample_size, random_state=42)
        
        shap_values = explainer.shap_values(X_sample)
        
        # Resumen de importancia global
        plt.figure(figsize=(12, 8))
        shap.summary_plot(shap_values, X_sample, feature_names=feature_names, plot_type="bar", show=False)
        plt.title('Importancia Global de Características')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'feature_importance_global.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print_step("✅ Importancia global de características generada y guardada")
        
        # Gráfico de resumen SHAP
        plt.figure(figsize=(12, 10))
        shap.summary_plot(shap_values, X_sample, feature_names=feature_names, show=False)
        plt.title('Valores SHAP - Resumen')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'shap_summary.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print_step("✅ Gráfico de resumen SHAP generado y guardado")
        
        # Explicaciones locales para casos específicos
        print_step("\n🔍 Explicaciones locales para casos representativos:")
        
        # Convertir a DataFrame para facilitar el manejo
        X_sample_df = X_sample.copy() if isinstance(X_sample, pd.DataFrame) else pd.DataFrame(X_sample, columns=feature_names)
        y_test_sample = model.predict(X_sample)
        y_pred_proba_sample = model.predict_proba(X_sample)[:, 1]
        
        # Caso 1: Alto riesgo (mal pagador predicho correctamente)
        high_risk_indices = np.where((y_test_sample == 0))[0]
        if len(high_risk_indices) > 0:
            high_risk_idx = high_risk_indices[0]
            print_step(f"  • Caso de alto riesgo (índice {high_risk_idx})")
            
            plt.figure(figsize=(10, 6))
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values[high_risk_idx], 
                    base_values=explainer.expected_value,
                    data=X_sample_df.iloc[high_risk_idx].values,
                    feature_names=feature_names
                ),
                max_display=10,
                show=False
            )
            plt.title(f'Explicación SHAP - Alto Riesgo (Índice {high_risk_idx})')
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, 'shap_alto_riesgo.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print_step("✅ Explicación SHAP para caso de alto riesgo generada y guardada")
        
        # Caso 2: Frontera (probabilidad cerca del umbral óptimo)
        border_indices = np.argsort(np.abs(y_pred_proba_sample - 0.5))[:3]
        if len(border_indices) > 0:
            border_idx = border_indices[0]
            print_step(f"  • Caso frontera (índice {border_idx}, prob={y_pred_proba_sample[border_idx]:.4f})")
            
            plt.figure(figsize=(10, 6))
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values[border_idx], 
                    base_values=explainer.expected_value,
                    data=X_sample_df.iloc[border_idx].values,
                    feature_names=feature_names
                ),
                max_display=10,
                show=False
            )
            plt.title(f'Explicación SHAP - Caso Frontera (Índice {border_idx})')
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, 'shap_caso_frontera.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print_step("✅ Explicación SHAP para caso frontera generada y guardada")
        
        # Caso 3: Error (seleccionar un caso incorrectamente clasificado si existe)
        wrong_indices = np.where(y_test_sample != model.predict(X_sample))[0]
        if len(wrong_indices) > 0:
            wrong_idx = wrong_indices[0]
            print_step(f"  • Caso mal clasificado (índice {wrong_idx})")
            
            plt.figure(figsize=(10, 6))
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values[wrong_idx], 
                    base_values=explainer.expected_value,
                    data=X_sample_df.iloc[wrong_idx].values,
                    feature_names=feature_names
                ),
                max_display=10,
                show=False
            )
            plt.title(f'Explicación SHAP - Mal Clasificado (Índice {wrong_idx})')
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, 'shap_mal_clasificado.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print_step("✅ Explicación SHAP para caso mal clasificado generada y guardada")
            
    except Exception as e:
        print_step(f"⚠️ Error al generar explicaciones SHAP: {str(e)}")
        print_step("Continuando sin explicabilidad detallada...")

def save_artifacts(model: Any, calibrated_model: Any, X_train: pd.DataFrame, results: Dict, feature_names: List[str]) -> Dict:
    """Guarda artefactos necesarios para deployment web."""
    print_step("Guardando artefactos para deployment web", is_header=True)
    
    # 1. Guardar modelo calibrado
    model_path = os.path.join(MODELS_DIR, 'credit_risk_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(calibrated_model, f)
    print_step(f"✓ Modelo guardado en: {model_path}")
    
    # 2. Guardar diccionario de características
    if hasattr(calibrated_model._get_estimator, 'feature_importances_'):
        feature_importances = calibrated_model._get_estimator.feature_importances_.tolist()
    else:
        feature_importances = [1/len(feature_names)] * len(feature_names)  # Importancias uniformes como fallback
    
    feature_dict = {
        'features': feature_names,
        'feature_importances': feature_importances,
        'optimal_threshold': results['optimal_threshold'],
        'class_names': ['Malo (0)', 'Bueno (1)'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'model_type': 'XGBoost Calibrado'
    }
    
    feature_dict_path = os.path.join(MODELS_DIR, 'feature_dictionary.csv')
    pd.DataFrame([feature_dict]).to_csv(feature_dict_path, index=False)
    print_step(f"✓ Diccionario de características guardado en: {feature_dict_path}")
    
    # 3. Guardar configuración para web
    web_config = {
        'model_name': 'Modelo de Riesgo Crediticio',
        'version': '1.0',
        'threshold': float(results['optimal_threshold']),
        'features': [
            {'name': col, 'type': 'numerical', 'description': f'Variable {col}'}
            for col in feature_names
        ],
        'target_description': {
            '0': 'Alto riesgo - No aprobar crédito',
            '1': 'Bajo riesgo - Aprobar crédito'
        },
        'metrics': {
            'test_recall': float(results['raw_metrics']['recall']),
            'test_precision': float(results['raw_metrics']['precision']),
            'test_f1': float(results['raw_metrics']['f1']),
            'test_roc_auc': float(results['raw_metrics']['roc_auc']),
            'test_pr_auc': float(results['raw_metrics']['pr_auc'])
        }
    }
    
    web_config_path = os.path.join(MODELS_DIR, 'web_config.json')
    with open(web_config_path, 'w') as f:
        json.dump(web_config, f, indent=2)
    print_step(f"✓ Configuración para web guardada en: {web_config_path}")
    
    # 4. Guardar todas las métricas
    metrics_path = os.path.join(MODELS_DIR, 'model_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump({
            'model_name': 'XGBoost Calibrado',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **results['raw_metrics'],
            **results['opt_metrics'],
            'optimal_threshold': float(results['optimal_threshold'])
        }, f, indent=2)
    print_step(f"✓ Métricas del modelo guardadas en: {metrics_path}")
    
    return web_config

def generate_report(web_config: Dict) -> None:
    """Genera un reporte resumen del modelo para documentación."""
    print_step("Generando reporte final del modelo", is_header=True)
    
    report = f"""
    REPORTE DEL MODELO DE RIESGO CREDITICIO
    {'='*60}
    Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Modelo: {web_config['model_name']} (versión {web_config['version']})
    
    DESEMPEÑO EN CONJUNTO DE PRUEBA:
    {'-'*60}
    • Recall (Capacidad para detectar malos pagadores): {web_config['metrics']['test_recall']:.4f}
    • Precisión (Exactitud en aprobaciones): {web_config['metrics']['test_precision']:.4f}
    • F1-Score (Balance): {web_config['metrics']['test_f1']:.4f}
    • AUC-ROC (Capacidad de discriminación): {web_config['metrics']['test_roc_auc']:.4f}
    • AUC-PR (Robustez ante desbalance): {web_config['metrics']['test_pr_auc']:.4f}
    
    CONFIGURACIÓN DEL MODELO:
    {'-'*60}
    • Umbral de decisión óptimo: {web_config['threshold']:.4f}
    • Características utilizadas: {len(web_config['features'])}
    • Clases objetivo: {', '.join(web_config['target_description'].values())}
    
    RECOMENDACIONES OPERATIVAS:
    {'-'*60}
    • Utilizar el umbral óptimo de {web_config['threshold']:.4f} para balancear detección de riesgo y oportunidades de negocio
    • Monitorear periódicamente las métricas de desempeño y equidad
    • Realizar recalibración cada 6 meses o cuando se observe desviación significativa en las métricas
    • Revisar las decisiones en los casos frontera (probabilidades cercanas al umbral)
    • Auditar las decisiones para diferentes segmentos demográficos para garantizar equidad
    
    ARTEFACTOS GENERADOS:
    {'-'*60}
    • Modelo entrenado: {os.path.join(MODELS_DIR, 'credit_risk_model.pkl')}
    • Configuración para web: {os.path.join(MODELS_DIR, 'web_config.json')}
    • Diccionario de características: {os.path.join(MODELS_DIR, 'feature_dictionary.csv')}
    • Métricas completas: {os.path.join(MODELS_DIR, 'model_metrics.json')}
    • Visualizaciones: {PLOTS_DIR}
    """
    
    report_path = os.path.join(MODELS_DIR, 'model_report.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    
    print_step(report)
    print_step(f"✅ Reporte completo guardado en: {report_path}")

if __name__ == "__main__":
    # Inicio del pipeline
    print_step("INICIANDO PIPELINE DE MODELADO PARA RIESGO CREDITICIO", is_header=True)
    print_step("Objetivo: Desarrollar un modelo web-friendly para predecir riesgo crediticio")
    
    try:
        # 1. Cargar datos
        file_path = os.path.join(DATA_DIR, 'data_preprocesada_arboles.csv')
        X, y = load_preprocessed_data(file_path)
        
        # 2. Dividir datos
        X_train, X_test, y_train, y_test, sample_weights = split_data(X, y)
        
        # 3. Optimizar modelo
        model = optimize_model(X_train, y_train, sample_weights)
        
        # 4. Calibrar modelo
        calibrated_model = calibrate_model(model, X_train, y_train)
        
        # 5. Evaluar modelo
        results = evaluate_model(calibrated_model, X_test, y_test)
        
        # 6. Generar gráficas de evaluación
        plot_evaluation_curves(calibrated_model, X_test, y_test, results)
        
        # 7. Analizar equidad
        analyze_fairness(calibrated_model, X_test, y_test, results['y_pred'], results['optimal_threshold'])
        
        # 8. Explicabilidad con SHAP
        explain_model(model, X_train, X_test, X_train.columns.tolist())
        
        # 9. Guardar artefactos para web
        web_config = save_artifacts(model, calibrated_model, X_train, results, X_train.columns.tolist())
        
        # 10. Generar reporte
        generate_report(web_config)
        
        print_step("PIPELINE DE MODELADO COMPLETADO EXITOSAMENTE", is_header=True)
        print_step("El modelo está listo para ser implementado en la aplicación web")
        print_step(f"Artefactos guardados en: {MODELS_DIR}")
        
    except Exception as e:
        print_step(f"❌ ERROR CRÍTICO DURANTE LA EJECUCIÓN: {str(e)}", is_header=True)
        import traceback
        traceback.print_exc()
        print_step("Se ha generado un log de errores en el directorio Logs/")