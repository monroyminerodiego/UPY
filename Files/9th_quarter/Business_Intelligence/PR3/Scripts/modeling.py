# modeling.py
"""
Módulo para entrenamiento, evaluación y explicabilidad del modelo XGBoost
para el dataset German Credit. Implementa el modelo recomendado por el 
lazy benchmark con las mejores prácticas de calibración, explicabilidad y equidad.
"""

from fpdf import FPDF
import datetime
import os
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve
)
from xgboost import XGBClassifier
import shap
import warnings
warnings.filterwarnings('ignore')

# Configuración inicial
RANDOM_STATE = 42
TEST_SIZE = 0.3
np.random.seed(RANDOM_STATE)

def load_preprocessed_data(filepath):
    """
    Carga los datos preprocesados del flujo 'arboles' recomendado en el benchmark.
    
    Args:
        filepath (str): Ruta al archivo CSV preprocesado
        
    Returns:
        X (pd.DataFrame): Features independientes
        y (pd.Series): Variable objetivo (0=good, 1=bad)
    """
    print(f"Cargando datos preprocesados desde: {filepath}")
    df = pd.read_csv(filepath)
    
    # Verificar si existe la columna target
    target_col = None
    possible_targets = ['target', 'target_binary', 'class']
    for col in possible_targets:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        raise ValueError("No se encontró columna objetivo en los datos preprocesados")
    
    # Asumiendo que la variable objetivo está codificada como 1=good, 2=bad
    # La convertimos a formato binario 0=good, 1=bad para facilitar el modelado
    if df[target_col].nunique() == 2:
        if set(df[target_col].unique()) == {1, 2}:
            df['target_binary'] = df[target_col].map({1: 0, 2: 1})  # 0=good (no default), 1=bad (default)
            y = df['target_binary']
        else:
            y = df[target_col]
        X = df.drop([target_col, 'target_binary'], axis=1, errors='ignore')
    else:
        raise ValueError(f"La columna objetivo '{target_col}' no tiene formato esperado (valores únicos: {df[target_col].unique()})")
    
    print(f"Dimensión de features: {X.shape}")
    print(f"Distribución de clases: {y.value_counts(normalize=True)}")
    
    return X, y

def train_calibrate_xgboost(X_train, y_train, X_val, y_val):
    """
    Entrena y calibra un modelo XGBoost según la recomendación del lazy benchmark.
    
    Args:
        X_train, y_train: Datos de entrenamiento
        X_val, y_val: Datos de validación para calibración
        
    Returns:
        tuple: (modelo_calibrado, modelo_base, información_del_modelo)
    """
    print("Entrenando y calibrando modelo XGBoost...")
    
    # Configurar XGBoost con parámetros iniciales optimizados para este problema
    # Considerando el desbalance de clases (70% good, 30% bad)
    scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
    
    xgb = XGBClassifier(
        random_state=RANDOM_STATE,
        eval_metric='logloss',
        use_label_encoder=False,
        scale_pos_weight=scale_pos_weight,
        # Parámetros iniciales para evitar overfitting
        max_depth=5,
        learning_rate=0.1,
        n_estimators=100,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0.1
    )
    
    # Entrenamiento inicial
    xgb.fit(X_train, y_train)
    
    # Calibración de probabilidades usando isotonic regression
    xgb_calibrated = CalibratedClassifierCV(xgb, method='isotonic', cv='prefit')
    xgb_calibrated.fit(X_val, y_val)
    
    # Información del modelo
    model_info = {
        'base_model': xgb,
        'calibrated_model': xgb_calibrated,
        'scale_pos_weight': scale_pos_weight
    }
    
    print("Entrenamiento y calibración completados")
    return xgb_calibrated, xgb, model_info

def optimize_threshold(model, X_val, y_val, metric='f1', optimize_for='recall'):
    """
    Optimiza el umbral de decisión para maximizar una métrica específica.
    
    Args:
        model: Modelo calibrado
        X_val, y_val: Datos de validación
        metric (str): Métrica a optimizar ('f1', 'recall', 'precision')
        optimize_for (str): 'recall' para minimizar falsos negativos (clientes buenos clasificados como malos)
                           'precision' para minimizar falsos positivos (clientes malos clasificados como buenos)
        
    Returns:
        float: Mejor umbral encontrado
    """
    # Obtener probabilidades de la clase positiva (riesgo)
    y_proba = model.predict_proba(X_val)[:, 1]
    
    best_threshold = 0.5
    best_score = 0
    
    # Probar diferentes umbrales
    thresholds = np.arange(0.1, 0.9, 0.01)
    
    if optimize_for == 'recall':
        # Priorizar recall para minimizar falsos negativos (riesgo para el banco)
        for threshold in thresholds:
            y_pred = (y_proba >= threshold).astype(int)
            score = recall_score(y_val, y_pred)
            if score > best_score:
                best_score = score
                best_threshold = threshold
    elif optimize_for == 'precision':
        # Priorizar precision para minimizar falsos positivos (rechazar buenos clientes)
        for threshold in thresholds:
            y_pred = (y_proba >= threshold).astype(int)
            score = precision_score(y_val, y_pred)
            if score > best_score:
                best_score = score
                best_threshold = threshold
    else:
        # Balance F1
        for threshold in thresholds:
            y_pred = (y_proba >= threshold).astype(int)
            score = f1_score(y_val, y_pred)
            if score > best_score:
                best_score = score
                best_threshold = threshold
    
    print(f"Mejor umbral para {optimize_for}: {best_threshold:.4f} con {metric} score {best_score:.4f}")
    return best_threshold, best_score

def evaluate_model(model, X_test, y_test, threshold=0.5, model_name="XGBoost", output_dir='Docs'):
    """
    Evalúa el modelo usando múltiples métricas y genera visualizaciones.
    
    Args:
        model: Modelo entrenado
        X_test, y_test: Conjunto de prueba
        threshold (float): Umbral de decisión
        model_name (str): Nombre del modelo para las visualizaciones
        output_dir (str): Directorio donde guardar las gráficas
        
    Returns:
        dict: Resultados de evaluación
    """
    print(f"\nEvaluando {model_name} con umbral={threshold:.4f}...")
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Predicciones y probabilidades
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)
    
    # Calcular métricas
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba),
        'pr_auc': average_precision_score(y_test, y_proba),
        'threshold': threshold,
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    
    # Mostrar métricas principales
    print(f"Métricas para {model_name}:")
    print(f"  - Accuracy: {metrics['accuracy']:.4f}")
    print(f"  - Precision: {metrics['precision']:.4f}")
    print(f"  - Recall: {metrics['recall']:.4f}")
    print(f"  - F1 Score: {metrics['f1']:.4f}")
    print(f"  - ROC AUC: {metrics['roc_auc']:.4f}")
    print(f"  - PR AUC: {metrics['pr_auc']:.4f}")
    print(f"\nMatriz de Confusión:")
    print(metrics['confusion_matrix'])
    
    # Graficar curvas ROC y PR
    plt.figure(figsize=(15, 6))
    
    # Curva ROC
    plt.subplot(1, 2, 1)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.plot(fpr, tpr, label=f"{model_name} (AUC={metrics['roc_auc']:.3f})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Curva ROC')
    plt.legend()
    
    # Curva Precision-Recall
    plt.subplot(1, 2, 2)
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    plt.plot(recall, precision, label=f"{model_name} (AUC={metrics['pr_auc']:.3f})")
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Curva Precision-Recall')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_curves.png'))
    plt.close()
    
    # Gráfica de calibración
    plt.figure(figsize=(10, 8))
    prob_true, prob_pred = calibration_curve(y_test, y_proba, n_bins=10)
    
    plt.plot(prob_pred, prob_true, 's-', label=f"{model_name}")
    plt.plot([0, 1], [0, 1], 'k--', label="Perfectamente calibrado")
    plt.xlabel('Probabilidad promedio predicha')
    plt.ylabel('Fracción de positivos')
    plt.title('Curva de Calibración')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'calibration_curve.png'))
    plt.close()
    
    return {
        'metrics': metrics,
        'y_proba': y_proba,
        'y_pred': y_pred
    }

def explain_model_global(model, X_train, feature_names, output_dir='Docs'):
    """
    Genera explicaciones globales para el modelo XGBoost.
    
    Args:
        model: Modelo entrenado (puede ser calibrado o no)
        X_train: Datos de entrenamiento
        feature_names: Nombres de las características
        output_dir (str): Directorio donde guardar las gráficas
    
    Returns:
        dict: Resultados de la explicabilidad global
    """
    print("\nGenerando explicaciones globales para XGBoost...")
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    explanations = {}
    
    # Obtener el modelo base (manejar tanto modelo calibrado como no calibrado)
    if hasattr(model, 'estimator'):
        # Para modelos calibrados
        base_model = model.estimator
    elif hasattr(model, 'base_estimator'):
        # Para backward compatibility
        base_model = model.base_estimator
    else:
        # Asumir que es el modelo base directamente
        base_model = model
    
    # Importancia de características
    importances = base_model.feature_importances_
    
    # Crear DataFrame con importancias
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    explanations['feature_importance'] = importance_df
    
    # Mostrar top 15 características
    print("\nTop 15 características más importantes:")
    print(importance_df.head(15))
    
    # Visualización de importancia
    plt.figure(figsize=(12, 10))
    sns.barplot(x='importance', y='feature', data=importance_df.head(15))
    plt.title('Importancia de Características - XGBoost')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_importance.png'))
    plt.close()
    
    # SHAP values para explicabilidad global
    print("Calculando valores SHAP para explicabilidad global...")
    explainer = shap.TreeExplainer(base_model)
    shap_values = explainer.shap_values(X_train)
    
    # Resumen SHAP
    plt.figure(figsize=(12, 10))
    shap.summary_plot(shap_values, X_train, feature_names=feature_names, show=False)
    plt.title('Resumen de Valores SHAP')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'shap_summary.png'))
    plt.close()
    
    # Dependence plots para las top 3 características
    top_features = importance_df.head(3)['feature'].values
    for i, feature in enumerate(top_features, 1):
        plt.figure(figsize=(10, 8))
        shap.dependence_plot(feature, shap_values, X_train, feature_names=feature_names, show=False)
        plt.title(f'Dependencia SHAP: {feature}')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'shap_dependence_{feature.replace(" ", "_")}.png'))
        plt.close()
    
    explanations['shap_explainer'] = explainer
    explanations['shap_values'] = shap_values
    explanations['base_model'] = base_model  # Guardar referencia al modelo base
    
    return explanations

def explain_model_local(model, X_test, y_test, y_pred, y_proba, shap_explainer, output_dir='Docs', case_indices=None):
    """
    Genera explicaciones locales para casos específicos usando SHAP.
    
    Args:
        model: Modelo entrenado
        X_test: Datos de prueba
        y_test: Etiquetas reales
        y_pred: Predicciones binarias
        y_proba: Probabilidades de predicción
        shap_explainer: Explainer de SHAP precalculado
        output_dir (str): Directorio donde guardar las gráficas
        case_indices: Índices de casos específicos para explicar
        
    Returns:
        dict: Explicaciones locales para los casos seleccionados
    """
    print("\nGenerando explicaciones locales con SHAP...")
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    local_explanations = {}
    feature_names = X_test.columns
    
    # Seleccionar casos representativos si no se especifican índices
    if case_indices is None:
        # Caso mal clasificado
        misclassified = np.where(y_pred != y_test)[0]
        misclassified_idx = misclassified[0] if len(misclassified) > 0 else None
        
        if misclassified_idx is None:
            print("No se encontraron casos mal clasificados en el conjunto de prueba")
        
        # Caso "frontera" (probabilidad cercana al umbral)
        border_cases = np.argsort(np.abs(y_proba - 0.5))[:10]
        border_idx = None
        for idx in border_cases:
            if y_pred[idx] != y_test.iloc[idx]:
                border_idx = idx
                break
        if border_idx is None:
            border_idx = border_cases[0]
        
        # Caso de alto riesgo correctamente clasificado
        high_risk = np.where((y_pred == 1) & (y_test == 1))[0]
        high_risk_idx = high_risk[0] if len(high_risk) > 0 else None
        
        case_indices = {
            'misclassified': misclassified_idx,
            'border': border_idx,
            'high_risk': high_risk_idx
        }
    
    print(f"Índices de casos seleccionados: {case_indices}")
    
    for case_type, idx in case_indices.items():
        if idx is None or idx >= len(X_test):
            print(f"No se encontró un caso de tipo '{case_type}'")
            continue
        
        case = X_test.iloc[idx]
        true_label = y_test.iloc[idx]
        pred_label = y_pred[idx]
        pred_proba = y_proba[idx]
        
        print(f"\nExplicando caso '{case_type}' (índice {idx}):")
        print(f"  - Probabilidad de riesgo: {pred_proba:.4f}")
        print(f"  - Predicción: {'Riesgo Alto' if pred_label == 1 else 'Riesgo Bajo'}")
        print(f"  - Etiqueta real: {'Riesgo Alto' if true_label == 1 else 'Riesgo Bajo'}")
        
        explanation = {
            'case_type': case_type,
            'features': case.to_dict(),
            'true_label': true_label,
            'pred_label': pred_label,
            'pred_proba': pred_proba
        }
        
        # Calcular valores SHAP para este caso específico
        shap_values = shap_explainer.shap_values(case.values.reshape(1, -1))[0]
        
        # Crear visualización SHAP force plot
        plt.figure(figsize=(20, 4))
        shap.force_plot(
            shap_explainer.expected_value, 
            shap_values, 
            case.values.reshape(1, -1), 
            feature_names=feature_names,
            matplotlib=True,
            show=False
        )
        plt.title(f'Explicación SHAP - Caso {case_type} (índice {idx})')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'shap_force_{case_type}.png'), bbox_inches='tight')
        plt.close()
        
        # Guardar valores SHAP para este caso
        explanation['shap_values'] = pd.Series(shap_values, index=feature_names)
        
        local_explanations[case_type] = explanation
        
        # Mostrar las características más influyentes para este caso
        abs_shap = np.abs(shap_values)
        top_indices = np.argsort(abs_shap)[::-1][:5]
        print(f"  Top 5 características influyentes para este caso:")
        for i in top_indices:
            feature = feature_names[i]
            value = case.iloc[i]
            shap_val = shap_values[i]
            direction = "aumenta" if shap_val > 0 else "disminuye"
            print(f"    - {feature} = {value}: {direction} el riesgo ({shap_val:.4f})")
    
    return local_explanations

def evaluate_fairness(model, X_test, y_test, y_pred, sensitive_attributes=['age'], output_dir='Docs'):
    """
    Evalúa la equidad del modelo en función de atributos sensibles.
    
    Args:
        model: Modelo entrenado
        X_test: Datos de prueba
        y_test: Etiquetas reales
        y_pred: Predicciones binarias
        sensitive_attributes (list): Lista de atributos sensibles para evaluar equidad
        output_dir (str): Directorio donde guardar las gráficas
        
    Returns:
        dict: Métricas de equidad por grupo
    """
    print("\nEvaluando equidad del modelo...")
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    fairness_results = {}
    
    for sensitive_attr in sensitive_attributes:
        print(f"\nAnalizando equidad según '{sensitive_attr}'...")
        
        # Verificar si el atributo existe en los datos
        if sensitive_attr not in X_test.columns:
            print(f"  Advertencia: '{sensitive_attr}' no encontrado en los datos de prueba")
            continue
        
        # Crear grupos para el atributo sensible
        if sensitive_attr == 'age':
            # Crear grupos de edad si es atributo numérico
            if X_test[sensitive_attr].dtype in ['int64', 'float64']:
                bins = [0, 30, 50, 100]
                labels = ['joven (<30)', 'adulto (30-50)', 'mayor (>50)']
                X_test_copy = X_test.copy()
                X_test_copy['age_group'] = pd.cut(X_test_copy[sensitive_attr], bins=bins, labels=labels)
                group_col = 'age_group'
            else:
                group_col = sensitive_attr
        else:
            group_col = sensitive_attr
        
        # Calcular métricas por grupo
        grouped_results = {}
        groups = X_test_copy[group_col].unique() if 'X_test_copy' in locals() else X_test[group_col].unique()
        
        for group in groups:
            if pd.isna(group):
                continue
                
            group_indices = X_test_copy[group_col] == group if 'X_test_copy' in locals() else X_test[group_col] == group
            group_size = np.sum(group_indices)
            
            if group_size < 30:  # Tamaño mínimo para estadísticas significativas
                continue
            
            group_y_true = y_test[group_indices]
            group_y_pred = y_pred[group_indices]
            
            # Calcular métricas por grupo
            if len(np.unique(group_y_true)) < 2:
                print(f"  Advertencia: grupo '{group}' solo contiene una clase. Saltando.")
                continue
                
            group_metrics = {
                'size': int(group_size),
                'positive_rate': float(np.mean(group_y_pred)),  # Tasa de clasificación como riesgo alto
                'true_positive_rate': float(recall_score(group_y_true, group_y_pred)),
                'false_positive_rate': float(np.sum((group_y_pred == 1) & (group_y_true == 0)) / 
                                          np.sum(group_y_true == 0)) if np.sum(group_y_true == 0) > 0 else 0,
                'precision': float(precision_score(group_y_true, group_y_pred))
            }
            
            grouped_results[group] = group_metrics
        
        if not grouped_results:
            print(f"  No se pudieron calcular métricas para '{sensitive_attr}'")
            continue
        
        # Calcular diferencias de equidad
        groups = list(grouped_results.keys())
        positive_rates = [grouped_results[g]['positive_rate'] for g in groups]
        tpr_rates = [grouped_results[g]['true_positive_rate'] for g in groups]
        
        demographic_parity = max(positive_rates) - min(positive_rates)
        equal_opportunity = max(tpr_rates) - min(tpr_rates)
        
        print(f"\nMétricas de Equidad para '{sensitive_attr}':")
        print(f"  - Demographic Parity (máx diferencia en tasas de positivos): {demographic_parity:.4f}")
        print(f"  - Equal Opportunity (máx diferencia en TPR): {equal_opportunity:.4f}")
        
        # Visualización de equidad
        plt.figure(figsize=(14, 7))
        metrics_df = pd.DataFrame(grouped_results).T
        
        # Gráfico de barras para tasas por grupo
        ax = metrics_df[['positive_rate', 'true_positive_rate', 'false_positive_rate']].plot(
            kind='bar', 
            figsize=(14, 7),
            color=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
        
        ax.set_title(f'Equidad por Grupo - {sensitive_attr}', fontsize=16)
        ax.set_ylabel('Tasa', fontsize=12)
        ax.set_xlabel('Grupo', fontsize=12)
        ax.legend([
            'Tasa de Riesgo Alto (DP)', 
            'Tasa Verdaderos Positivos (EO)',
            'Tasa Falsos Positivos'
        ])
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'fairness_{sensitive_attr.replace(" ", "_")}.png'))
        plt.close()
        
        fairness_results[sensitive_attr] = {
            'group_metrics': grouped_results,
            'demographic_parity': demographic_parity,
            'equal_opportunity': equal_opportunity
        }
    
    return fairness_results

def save_model_for_production(model, threshold, metrics, feature_names, output_dir='models'):
    """
    Guarda el modelo entrenado y sus metadatos para producción.
    
    Args:
        model: Modelo entrenado
        threshold: Umbral óptimo de decisión
        metrics: Métricas de evaluación
        feature_names: Nombres de las características
        output_dir (str): Directorio de salida
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtener el modelo base para guardar
    if hasattr(model, 'estimator'):
        base_model = model.estimator
    else:
        base_model = model
    
    # Guardar el modelo completo
    model_path = os.path.join(output_dir, "credit_risk_model.pkl")
    joblib.dump({
        'model': model,
        'base_model': base_model,  # Guardar también el modelo base
        'threshold': threshold,
        'metrics': metrics,
        'feature_names': feature_names.tolist(),
        'metadata': {
            'model_type': 'XGBoost',
            'calibration_method': 'isotonic' if hasattr(model, 'estimator') else 'none',
            'random_state': RANDOM_STATE,
            'training_date': pd.Timestamp.now().strftime('%Y-%m-%d')
        }
    }, model_path)
    print(f"Modelo guardado en {model_path}")
    
    # Guardar información adicional para la aplicación web
    web_config = {
        'model_path': model_path,
        'threshold': threshold,
        'feature_names': feature_names.tolist(),
        'roc_auc': metrics['roc_auc'],
        'recall': metrics['recall'],
        'precision': metrics['precision']
    }
    
    import json
    config_path = os.path.join(output_dir, "web_config.json")
    with open(config_path, 'w') as f:
        json.dump(web_config, f, indent=2)
    print(f"Configuración para web guardada en {config_path}")
    
    # Generar archivo de características para documentación
    features_df = pd.DataFrame({
        'feature': feature_names,
        'description': [''] * len(feature_names),
        'type': [''] * len(feature_names)
    })
    features_df.to_csv(os.path.join(output_dir, "feature_dictionary.csv"), index=False)
    print("Diccionario de características generado")

def generate_business_report(metrics, fairness_results, threshold, output_dir='Docs'):
    """
    Genera un informe ejecutivo con las métricas clave y recomendaciones de negocio.
    """
    print("\n" + "="*60)
    print("INFORME EJECUTIVO - MODELO DE RIESGO DE CRÉDITO")
    print("="*60)
    
    print(f"\n📊 DESEMPEÑO DEL MODELO")
    print(f"   * ROC AUC: {metrics['roc_auc']:.4f} (objetivo > 0.75)")
    print(f"   * F1 Score: {metrics['f1']:.4f}")
    print(f"   * Recall: {metrics['recall']:.4f} (capacidad para detectar malos pagadores)")
    print(f"   * Precision: {metrics['precision']:.4f} (exactitud en identificar buenos clientes)")
    print(f"   * Umbral óptimo: {threshold:.4f}")
    
    print(f"\n💡 ANÁLISIS DE EQUIDAD")
    for attr, results in fairness_results.items():
        print(f"\n   Atributo: {attr}")
        print(f"   * Demographic Parity (diferencia máxima en aprobaciones): {results['demographic_parity']:.4f}")
        print(f"   * Equal Opportunity (diferencia máxima en detección de riesgo): {results['equal_opportunity']:.4f}")
        
        # Análisis por grupos - CORRECCIÓN: Cambiar 'metrics' por 'group_metric'
        group_metrics = results['group_metrics']
        print("   * Métricas por grupo:")
        for group, group_metric in group_metrics.items():  # Cambiado aquí
            print(f"      - {group} (n={group_metric['size']}):")
            print(f"        · Tasa de riesgo alto: {group_metric['positive_rate']:.4f}")
            print(f"        · Tasa de detección (TPR): {group_metric['true_positive_rate']:.4f}")
    
    print(f"\n✅ RECOMENDACIÓN OPERATIVA")
    print("   1. Implementar modelo XGBoost con umbral optimizado para recall")
    print("   2. Monitorear mensualmente: drift de datos, desempeño y equidad")
    print("   3. Reentrenar trimestralmente con nuevos datos")
    print("   4. Realizar auditoría de equidad semestralmente")
    print("   5. Documentar todas las decisiones para cumplimiento regulatorio")
    
    # Guardar el informe en un archivo de texto
    report_path = os.path.join(output_dir, "business_report.txt")
    with open(report_path, 'w') as f:
        f.write("INFORME EJECUTIVO - MODELO DE RIESGO DE CRÉDITO\n")
        f.write("="*60 + "\n")
        f.write(f"\nDESEMPEÑO DEL MODELO\n")
        f.write(f"* ROC AUC: {metrics['roc_auc']:.4f}\n")
        f.write(f"* F1 Score: {metrics['f1']:.4f}\n")
        f.write(f"* Recall: {metrics['recall']:.4f}\n")
        f.write(f"* Precision: {metrics['precision']:.4f}\n")
        f.write(f"* Umbral óptimo: {threshold:.4f}\n")
    
    print(f"\n📄 Informe ejecutivo guardado en: {report_path}")

def generate_pdf_report(metrics, fairness_results, threshold, feature_importance, 
                       local_explanations, output_dir='Docs'):
    """
    Genera un reporte PDF profesional con todos los resultados del modelo.
    
    Args:
        metrics: Métricas de evaluación del modelo
        fairness_results: Resultados de equidad
        threshold: Umbral óptimo
        feature_importance: DataFrame con importancia de características
        local_explanations: Explicaciones locales
        output_dir: Directorio de salida
    """
    try:
        from fpdf import FPDF
    except ImportError:
        print(" Instala fpdf para generar reportes PDF: pip install fpdf")
        return None
    
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'INFORME EJECUTIVO - MODELO DE RIESGO DE CRÉDITO', 0, 1, 'C')
    pdf.ln(5)
    
    # Fecha
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f'Generado el: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
    pdf.ln(10)
    
    # 1. RESUMEN EJECUTIVO
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '1. RESUMEN EJECUTIVO', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    # Calcular riesgo basado en métricas
    roc_auc = metrics['roc_auc']
    if roc_auc >= 0.8:
        riesgo = "BAJO"
        nivel_riesgo = "[BAJO RIESGO]"
    elif roc_auc >= 0.7:
        riesgo = "MODERADO"
        nivel_riesgo = "[MODERADO RIESGO]"
    else:
        riesgo = "ALTO"
        nivel_riesgo = "[ALTO RIESGO]"
    
    summary_text = f"""
    {nivel_riesgo}
    
    * ROC AUC: {metrics['roc_auc']:.4f} 
    * Recall: {metrics['recall']:.4f} 
    * Precision: {metrics['precision']:.4f}
    * Umbral óptimo: {threshold:.4f}
    
    El modelo muestra capacidad {'excelente' if roc_auc >= 0.8 else 'adecuada' if roc_auc >= 0.7 else 'limitada'} 
    para predecir el riesgo crediticio, con especial enfoque en la detección de clientes de alto riesgo 
    (recall del {metrics['recall']:.2%}).
    """
    
    pdf.multi_cell(0, 8, summary_text)
    pdf.ln(10)
    
    # 2. MÉTRICAS DE DESEMPEÑO
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. MÉTRICAS DE DESEMPEÑO', 0, 1)
    
    # Tabla de métricas
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(90, 10, 'Métrica', 1)
    pdf.cell(50, 10, 'Valor', 1)
    pdf.cell(50, 10, 'Interpretación', 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 10)
    metric_data = [
        ('ROC AUC', f"{metrics['roc_auc']:.4f}", "Capacidad discriminativa"),
        ('Precision', f"{metrics['precision']:.4f}", "Exactitud en riesgos altos"),
        ('Recall', f"{metrics['recall']:.4f}", "Detección de malos pagadores"),
        ('F1-Score', f"{metrics['f1']:.4f}", "Balance general"),
        ('Accuracy', f"{metrics['accuracy']:.4f}", "Precisión global")
    ]
    
    for metric, value, interpretation in metric_data:
        pdf.cell(90, 8, metric, 1)
        pdf.cell(50, 8, value, 1)
        pdf.cell(50, 8, interpretation, 1)
        pdf.ln()
    
    pdf.ln(10)
    
    # 3. ANÁLISIS DE EQUIDAD
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. ANÁLISIS DE EQUIDAD', 0, 1)
    
    for attr, results in fairness_results.items():
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'Atributo: {attr.upper()}', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        pdf.cell(0, 6, f'* Demographic Parity: {results["demographic_parity"]:.4f}', 0, 1)
        pdf.cell(0, 6, f'* Equal Opportunity: {results["equal_opportunity"]:.4f}', 0, 1)
        
        # Tabla de grupos
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(50, 8, 'Grupo', 1)
        pdf.cell(30, 8, 'Muestra', 1)
        pdf.cell(40, 8, 'Tasa Riesgo', 1)
        pdf.cell(40, 8, 'TPR', 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 9)
        for group, group_metric in results['group_metrics'].items():
            pdf.cell(50, 8, str(group), 1)
            pdf.cell(30, 8, str(group_metric['size']), 1)
            pdf.cell(40, 8, f"{group_metric['positive_rate']:.4f}", 1)
            pdf.cell(40, 8, f"{group_metric['true_positive_rate']:.4f}", 1)
            pdf.ln()
        
        pdf.ln(5)
    
    # 4. CARACTERÍSTICAS MÁS IMPORTANTES
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '4. CARACTERÍSTICAS MÁS IMPORTANTES', 0, 1)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 8, 'Característica', 1)
    pdf.cell(40, 8, 'Importancia', 1)
    pdf.ln()
    
    pdf.set_font('Arial', '', 9)
    top_features = feature_importance.head(10)
    for _, row in top_features.iterrows():
        # Acortar nombres largos
        feature_name = row['feature']
        if len(feature_name) > 40:
            feature_name = feature_name[:37] + "..."
        
        pdf.cell(100, 8, feature_name, 1)
        pdf.cell(40, 8, f"{row['importance']:.4f}", 1)
        pdf.ln()
    
    pdf.ln(10)
    
    # 5. EXPLICACIONES LOCALES
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '5. CASOS DE ESTUDIO', 0, 1)
    
    for case_type, explanation in local_explanations.items():
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'Caso: {case_type.upper()}', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        pdf.cell(0, 6, f'* Probabilidad: {explanation["pred_proba"]:.4f}', 0, 1)
        pdf.cell(0, 6, f'* Predicción: {"RIESGO ALTO" if explanation["pred_label"] == 1 else "RIESGO BAJO"}', 0, 1)
        pdf.cell(0, 6, f'* Real: {"RIESGO ALTO" if explanation["true_label"] == 1 else "RIESGO BAJO"}', 0, 1)
        
        # Top características influyentes
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 8, 'Factores determinantes:', 0, 1)
        pdf.set_font('Arial', '', 9)
        
        shap_vals = explanation['shap_values']
        # CORRECCIÓN: Convertir Series de pandas a numpy array para usar argsort
        shap_values_array = shap_vals.values
        top_indices = np.argsort(np.abs(shap_values_array))[::-1][:3]
        
        for i in top_indices:
            feature = shap_vals.index[i]
            value = explanation['features'].get(feature, 'N/A')
            shap_val = shap_vals.iloc[i]
            direction = "AUMENTA" if shap_val > 0 else "DISMINUYE"
            
            # Acortar nombres largos
            if len(feature) > 30:
                feature = feature[:27] + "..."
            
            pdf.cell(0, 6, f'   - {feature}: {direction} riesgo ({shap_val:.4f})', 0, 1)
        
        pdf.ln(5)
    
    # 6. RECOMENDACIONES
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '6. RECOMENDACIONES OPERATIVAS', 0, 1)
    
    recommendations = [
        "* IMPLEMENTAR modelo con supervisión mensual del desempeño",
        "* MONITOREAR equidad en decisiones crediticias trimestralmente",
        "* REENTRENAR modelo cada 6 meses con nuevos datos",
        "* AUDITORÍA de equidad semestral para cumplimiento regulatorio",
        "* DOCUMENTAR todas las decisiones de crédito para trazabilidad"
    ]
    
    pdf.set_font('Arial', '', 11)
    for rec in recommendations:
        pdf.cell(0, 8, rec, 0, 1)
    
    # Guardar PDF
    pdf_path = os.path.join(output_dir, "modelo_riesgo_crediticio_informe.pdf")
    pdf.output(pdf_path)
    print(f"📊 Reporte PDF generado: {pdf_path}")

    return pdf_path

def run_modeling_pipeline(data_path, output_dir='Docs'):
    """
    Ejecuta el pipeline completo de modelado según los requisitos y recomendaciones del lazy benchmark.
    
    Args:
        data_path (str): Ruta a los datos preprocesados
        output_dir (str): Directorio para guardar resultados
    """
    # 1. Cargar datos
    X, y = load_preprocessed_data(data_path)
    
    # 2. Dividir datos (estratificado por clase)
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    # División adicional para entrenamiento y calibración
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.2, random_state=RANDOM_STATE, stratify=y_train_val
    )
    
    print(f"\nTamaños de conjuntos:")
    print(f"  - Entrenamiento: {X_train.shape[0]}")
    print(f"  - Validación (para calibración): {X_val.shape[0]}")
    print(f"  - Prueba: {X_test.shape[0]}")
    
    # 3. Entrenar y calibrar modelo XGBoost
    model_calibrated, model_base, model_info = train_calibrate_xgboost(X_train, y_train, X_val, y_val)
    
    # 4. Optimizar umbral - priorizar recall para minimizar falsos negativos (riesgo para el banco)
    threshold, score = optimize_threshold(model_calibrated, X_val, y_val, 
                                          metric='recall', optimize_for='recall')
    
    # 5. Evaluar modelo en conjunto de prueba
    results = evaluate_model(model_calibrated, X_test, y_test, threshold, output_dir=output_dir)
    
    # 6. Explicabilidad global
    global_explanations = explain_model_global(model_calibrated, X_train, X_train.columns, output_dir=output_dir)
    
    # 7. Explicabilidad local
    local_explanations = explain_model_local(
        model_calibrated, 
        X_test, 
        y_test, 
        results['y_pred'], 
        results['y_proba'],
        global_explanations['shap_explainer'],
        output_dir=output_dir
    )
    
    # 8. Evaluación de equidad (usando edad como atributo sensible principal)
    fairness_results = evaluate_fairness(model_calibrated, X_test, y_test, results['y_pred'], 
                                       sensitive_attributes=['age'], output_dir=output_dir)
    
    # 9. Guardar modelo para producción (también en Docs para mantener todo organizado)
    models_dir = os.path.join(output_dir, 'models')
    save_model_for_production(
        model_calibrated, 
        threshold, 
        results['metrics'], 
        X_train.columns,
        models_dir
    )
    
    # 10. Generar informe ejecutivo (CORREGIDO)
    generate_business_report(results['metrics'], fairness_results, threshold, output_dir)
    
    # 11. Generar reporte PDF profesional
    pdf_path = generate_pdf_report(
        results['metrics'], 
        fairness_results, 
        threshold,
        global_explanations['feature_importance'],
        local_explanations,
        output_dir
    )
    
    print("\n✅ Pipeline de modelado completado exitosamente")
    print(f"📁 Resultados guardados en: {output_dir}")
    print(f"📊 Reporte PDF: {pdf_path}")
    
    return {
        'model': model_calibrated,
        'threshold': threshold,
        'metrics': results['metrics'],
        'fairness_results': fairness_results,
        'global_explanations': global_explanations,
        'local_explanations': local_explanations,
        'pdf_report_path': pdf_path
    }



if __name__ == "__main__":
    # Obtener la ruta del directorio del proyecto
    location_path = os.path.dirname(os.path.dirname(__file__))
    
    # Definir rutas usando location_path
    data_path = os.path.join(location_path, 'Data', 'processed', 'data_preprocesada_arboles.csv')
    output_dir = os.path.join(location_path, 'Docs')
    
    print(f"Directorio del proyecto: {location_path}")
    print(f"Ruta de datos: {data_path}")
    print(f"Directorio de salida: {output_dir}")
    
    # Ejecutar el pipeline completo
    results = run_modeling_pipeline(data_path, output_dir)