#!/usr/bin/env python3
"""
modeling.py
Script para entrenar y evaluar el modelo RidgeClassifierCV con preprocesamiento de 'arboles'
para el problema de riesgo crediticio. Genera todos los artefactos necesarios para la aplicación web.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import RidgeClassifierCV
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, average_precision_score,
                            confusion_matrix, roc_curve, precision_recall_curve)
from sklearn.preprocessing import StandardScaler
import joblib
import json
import time
import sys
from sklearn.utils.class_weight import compute_class_weight

print("=" * 80)
print("🚀 INICIANDO MODELADO - RIDGECLASSIFIERCV CON PREPROCESAMIENTO 'ARBOLES'")
print("=" * 80)

# Configurar rutas relativas al script actual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Directorio padre de Scripts/

print(f"📍 Directorio del script: {SCRIPT_DIR}")
print(f"🏠 Directorio raíz del proyecto: {PROJECT_ROOT}")

# Definir rutas usando la estructura del proyecto
DATA_DIR = os.path.join(PROJECT_ROOT, 'Data', 'processed')
DOCS_DIR = os.path.join(PROJECT_ROOT, 'Docs')
MODELS_DIR = os.path.join(DOCS_DIR, 'models')
PLOTS_DIR = os.path.join(DOCS_DIR, 'plots')

# Crear directorios si no existen
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

print("\n📁 Rutas configuradas:")
print(f"   - Datos procesados: {DATA_DIR}")
print(f"   - Modelos: {MODELS_DIR}")
print(f"   - Gráficas: {PLOTS_DIR}")

# Verificar que exista el archivo de datos
DATA_FILE = os.path.join(DATA_DIR, 'data_preprocesada_arboles.csv')
if not os.path.exists(DATA_FILE):
    print(f"\n❌ ERROR CRÍTICO: No se encontró el archivo de datos en {DATA_FILE}")
    print("Por favor verifica que:")
    print("1. Ejecutaste el preprocesamiento previamente")
    print("2. El archivo 'data_preprocesada_arboles.csv' existe en la carpeta Data/processed/")
    print("3. La estructura de carpetas es la correcta")
    sys.exit(1)

print(f"\n✅ Archivo de datos encontrado: {DATA_FILE}")

# Cargar datos preprocesados
print("\n" + "-" * 60)
print("📂 CARGANDO Y PREPARANDO DATOS")
print("-" * 60)
data = pd.read_csv(DATA_FILE)
print(f"✅ Datos cargados exitosamente. Shape: {data.shape}")

# Verificar columna target
if 'target' not in data.columns:
    print(f"\n❌ ERROR: No se encontró la columna 'target' en los datos")
    print(f"Columnas disponibles: {list(data.columns)}")
    sys.exit(1)

# Separar features y target
X = data.drop('target', axis=1)
y = data['target']

# Mostrar distribución de la clase
print("\n📊 Distribución de la variable objetivo:")
class_counts = y.value_counts()
class_dist = class_counts / len(y) * 100
print(f"   - Clase positiva (good/1): {class_dist.get(1, 0):.1f}% ({class_counts.get(1, 0)} muestras)")
print(f"   - Clase negativa (bad/0): {class_dist.get(0, 0):.1f}% ({class_counts.get(0, 0)} muestras)")

# División estratificada de datos
print("\n✂️ Dividiendo datos en entrenamiento y prueba (estratificado)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)
print(f"   - Tamaño entrenamiento: {X_train.shape[0]} muestras ({len(y_train)/len(y)*100:.1f}%)")
print(f"   - Tamaño prueba: {X_test.shape[0]} muestras ({len(y_test)/len(y)*100:.1f}%)")
print(f"   - Distribución en entrenamiento: good={sum(y_train)/len(y_train)*100:.1f}%, bad={(1-sum(y_train)/len(y_train))*100:.1f}%")
print(f"   - Distribución en prueba: good={sum(y_test)/len(y_test)*100:.1f}%, bad={(1-sum(y_test)/len(y_test))*100:.1f}%")

# Escalar los datos
print("\n⚖️ Escalando características...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✅ Características escaladas exitosamente")

# Configurar pesos de clase para manejar desbalance
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = {0: class_weights[0], 1: class_weights[1]}
print(f"\n⚖️ Pesos de clase calculados para manejar desbalance:")
print(f"   - Clase 0 (bad): {class_weight_dict[0]:.4f}")
print(f"   - Clase 1 (good): {class_weight_dict[1]:.4f}")

# Crear y entrenar el modelo base
print("\n" + "-" * 60)
print("⚙️ CONFIGURANDO Y ENTRENANDO MODELO BASE")
print("-" * 60)
print("Configurando RidgeClassifierCV...")

alphas = np.logspace(-3, 3, 10)  # Rango de alphas para regularización

ridge_cv = RidgeClassifierCV(
    alphas=alphas,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='average_precision',
    class_weight=class_weight_dict
)

print("\n🏋️ Entrenando modelo RidgeClassifierCV...")
start_time = time.time()
ridge_cv.fit(X_train_scaled, y_train)
training_time = time.time() - start_time
print(f"✅ Modelo base entrenado exitosamente en {training_time:.2f} segundos")

# Obtener el mejor alpha
best_alpha = ridge_cv.alpha_
print(f"   - Mejor alpha seleccionado: {best_alpha:.6f}")

# Calibrar el modelo
print("\n🔧 Calibrando probabilidades con Platt Scaling...")
calibrated_clf = CalibratedClassifierCV(
    estimator=ridge_cv,
    method='sigmoid',  # Platt scaling
    cv='prefit'  # Usar el modelo ya entrenado
)

start_calibration = time.time()
calibrated_clf.fit(X_train_scaled, y_train)
calibration_time = time.time() - start_calibration
print(f"✅ Modelo calibrado exitosamente en {calibration_time:.2f} segundos")

# Generar probabilidades calibradas
y_proba_train = calibrated_clf.predict_proba(X_train_scaled)[:, 1]
y_proba_test = calibrated_clf.predict_proba(X_test_scaled)[:, 1]

# Optimización del umbral de decisión
print("\n🔍 Optimizando umbral de decisión para maximizar F1-Score...")
thresholds = np.arange(0.1, 0.9, 0.01)
f1_scores = []

for thresh in thresholds:
    y_pred = (y_proba_train >= thresh).astype(int)
    f1_scores.append(f1_score(y_train, y_pred))

best_idx = np.argmax(f1_scores)
best_threshold = thresholds[best_idx]
best_f1 = f1_scores[best_idx]

print(f"   - Mejor umbral encontrado: {best_threshold:.3f}")
print(f"   - F1-Score máximo en entrenamiento: {best_f1:.4f}")

# Evaluar con diferentes umbrales
y_pred_default = calibrated_clf.predict(X_test_scaled)  # Umbral 0.5 por defecto
y_pred_opt = (y_proba_test >= best_threshold).astype(int)

# Calcular métricas para ambos umbrales
metrics_default = {
    'Accuracy': accuracy_score(y_test, y_pred_default),
    'Precision': precision_score(y_test, y_pred_default),
    'Recall': recall_score(y_test, y_pred_default),
    'F1': f1_score(y_test, y_pred_default),
    'ROC-AUC': roc_auc_score(y_test, y_proba_test),
    'PR-AUC': average_precision_score(y_test, y_proba_test)
}

metrics_opt = {
    'Accuracy': accuracy_score(y_test, y_pred_opt),
    'Precision': precision_score(y_test, y_pred_opt),
    'Recall': recall_score(y_test, y_pred_opt),
    'F1': f1_score(y_test, y_pred_opt),
    'ROC-AUC': roc_auc_score(y_test, y_proba_test),
    'PR-AUC': average_precision_score(y_test, y_proba_test)
}

print("\n" + "-" * 60)
print("🧪 EVALUACIÓN DEL MODELO")
print("-" * 60)
print("\n📈 Métricas de evaluación (umbral 0.5):")
for metric, value in metrics_default.items():
    print(f"   - {metric}: {value:.4f}")

print("\n📈 Métricas de evaluación (umbral optimizado):")
for metric, value in metrics_opt.items():
    print(f"   - {metric}: {value:.4f}")

# Generar y guardar matriz de confusión
print("\n📊 Generando matriz de confusión...")
def plot_confusion_matrix(y_true, y_pred, title, filename, threshold):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    
    # Usar matplotlib directamente (más robusto)
    plt.imshow(cm, interpolation='nearest', cmap='Blues')
    plt.colorbar()
    
    # Etiquetas
    classes = ['Bad (0)', 'Good (1)']
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    # Anotaciones
    fmt = 'd'
    thresh_val = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh_val else "black",
                    fontsize=14, fontweight='bold')
    
    plt.title(f'{title}\nUmbral: {threshold:.3f}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicción', fontsize=14)
    plt.ylabel('Real', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Matriz de confusión guardada: {filename}")

plot_confusion_matrix(y_test, y_pred_opt, 'Matriz de Confusión - RidgeClassifierCV', 'confusion_matrix_ridge.png', best_threshold)

# Curvas ROC y Precision-Recall
print("\n📉 Generando curvas ROC y Precision-Recall...")
def plot_roc_pr_curves(y_true, y_proba, title_suffix, filename_prefix):
    # Curva ROC
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = roc_auc_score(y_true, y_proba)
    
    plt.figure(figsize=(14, 6))
    
    # Subplot 1: ROC Curve
    plt.subplot(1, 2, 1)
    plt.plot(fpr, tpr, color='darkorange', lw=3, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random (AUC = 0.5)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Tasa de Falsos Positivos (1 - Especificidad)', fontsize=12)
    plt.ylabel('Tasa de Verdaderos Positivos (Sensitividad)', fontsize=12)
    plt.title(f'Curva ROC {title_suffix}', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Curva Precision-Recall
    precision, recall, _ = precision_recall_curve(y_true, y_proba)
    pr_auc = average_precision_score(y_true, y_proba)
    no_skill = len(y_true[y_true == 1]) / len(y_true)
    
    plt.subplot(1, 2, 2)
    plt.plot(recall, precision, color='blue', lw=3, label=f'PR curve (AUC = {pr_auc:.3f})')
    plt.axhline(y=no_skill, color='r', linestyle='--', lw=2, label=f'No Skill ({no_skill:.3f})')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall (Sensitividad)', fontsize=12)
    plt.ylabel('Precisión', fontsize=12)
    plt.title(f'Curva Precision-Recall {title_suffix}', fontsize=14, fontweight='bold')
    plt.legend(loc="lower left", fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f'{filename_prefix}_curves.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Curvas ROC y PR guardadas: {filename_prefix}_curves.png")

plot_roc_pr_curves(y_test, y_proba_test, f'(Umbral óptimo: {best_threshold:.3f})', 'ridge')

# Importancia de características
print("\n🔍 Analizando importancia de características...")
coef_importance = np.abs(ridge_cv.coef_[0])
feature_names = X.columns

# Crear DataFrame de importancia
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': coef_importance
}).sort_values('importance', ascending=False)

# Guardar importancia de características
feature_importance.to_csv(os.path.join(MODELS_DIR, 'feature_importance_ridge.csv'), index=False)
print("✅ Importancia de características guardada")

# Gráfico de importancia de características
print("\n📊 Generando gráfico de importancia de características...")
plt.figure(figsize=(14, 10))
top_features = feature_importance.head(15)

# Crear barras horizontales
y_pos = np.arange(len(top_features))
colors = plt.cm.viridis(np.linspace(0, 1, len(top_features)))

plt.barh(y_pos, top_features['importance'], color=colors, height=0.6)
plt.yticks(y_pos, top_features['feature'], fontsize=12)
plt.gca().invert_yaxis()  # Mayor importancia en la parte superior

plt.title('Top 15 Características más Importantes - RidgeClassifierCV', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Valor absoluto del coeficiente', fontsize=14)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'feature_importance_ridge.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico de importancia de características guardado")

# Curva de calibración
print("\n📊 Generando curva de calibración...")
plt.figure(figsize=(10, 8))
prob_true, prob_pred = calibration_curve(y_test, y_proba_test, n_bins=10)

plt.plot(prob_pred, prob_true, 's-', color='blue', lw=3, markersize=8, label='RidgeClassifierCV')
plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Perfectamente calibrado')
plt.xlabel('Probabilidad promedio predicha', fontsize=12)
plt.ylabel('Fracción de positivos', fontsize=12)
plt.title('Curva de Calibración - RidgeClassifierCV', fontsize=14, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'calibration_curve_ridge.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✅ Curva de calibración guardada")

# Guardar modelo y artefactos para producción web
print("\n" + "-" * 60)
print("💾 GUARDANDO ARTEFACTOS PARA PRODUCCIÓN WEB")
print("-" * 60)
print("Guardando modelo y artefactos para producción web...")

# Guardar scaler
joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler_ridge.pkl'))
print(f"✅ Scaler guardado: {os.path.join(MODELS_DIR, 'scaler_ridge.pkl')}")

# Guardar modelo calibrado
joblib.dump(calibrated_clf, os.path.join(MODELS_DIR, 'ridge_calibrated_model.pkl'))
print(f"✅ Modelo calibrado guardado: {os.path.join(MODELS_DIR, 'ridge_calibrated_model.pkl')}")

# Crear diccionario de características para la web
print("\n📝 Creando diccionario de características...")
feature_dict = {}
for col in X.columns:
    # Inferir tipo de variable
    if pd.api.types.is_numeric_dtype(X[col]):
        if X[col].nunique() < 10:
            feature_type = 'numérico discreto'
        else:
            feature_type = 'numérico continuo'
    else:
        feature_type = 'categórico'
    
    feature_dict[col] = {
        'name': col,
        'type': feature_type,
        'description': f'Característica derivada de procesamiento de {col.split("_")[0]}' if "_" in col else f'Característica {col}',
        'min': float(X[col].min()) if pd.api.types.is_numeric_dtype(X[col]) else None,
        'max': float(X[col].max()) if pd.api.types.is_numeric_dtype(X[col]) else None,
        'mean': float(X[col].mean()) if pd.api.types.is_numeric_dtype(X[col]) else None,
        'std': float(X[col].std()) if pd.api.types.is_numeric_dtype(X[col]) else None,
        'original_feature': col.split("_")[0] if "_" in col else col
    }

# Guardar diccionario de características
with open(os.path.join(MODELS_DIR, 'feature_dictionary.json'), 'w') as f:
    json.dump(feature_dict, f, indent=2)
print(f"✅ Diccionario de características guardado: {os.path.join(MODELS_DIR, 'feature_dictionary.json')}")

# Configuración para la aplicación web
print("\n⚙️ Creando configuración para aplicación web...")
web_config = {
    'model_name': 'RidgeClassifierCV (Preprocesamiento Arboles)',
    'model_type': 'RidgeClassifierCV with Platt Scaling',
    'best_threshold': float(best_threshold),
    'default_threshold': 0.5,
    'metrics': {
        'training': {
            'f1_optimized': float(best_f1),
            'best_threshold': float(best_threshold)
        },
        'test': {
            'default_threshold': {k: float(v) for k, v in metrics_default.items()},
            'optimized_threshold': {k: float(v) for k, v in metrics_opt.items()}
        }
    },
    'class_names': ['Bad (Riesgo Alto)', 'Good (Riesgo Bajo)'],
    'feature_names': X.columns.tolist(),
    'target_name': 'Credit Risk',
    'training_time': float(training_time),
    'calibration_time': float(calibration_time),
    'data_shape': {
        'total_samples': len(data),
        'features': X.shape[1],
        'train_samples': len(X_train),
        'test_samples': len(X_test)
    },
    'calibration_method': 'sigmoid (Platt scaling)',
    'best_alpha': float(best_alpha),
    'class_weights': {str(k): float(v) for k, v in class_weight_dict.items()},
    'created_at': time.strftime("%Y-%m-%d %H:%M:%S")
}

# Guardar configuración web
with open(os.path.join(MODELS_DIR, 'web_config.json'), 'w') as f:
    json.dump(web_config, f, indent=2)
print(f"✅ Configuración web guardada: {os.path.join(MODELS_DIR, 'web_config.json')}")

# Guardar feature importance para la web
feature_importance_web = []
for idx, row in feature_importance.head(20).iterrows():
    feature_importance_web.append({
        'rank': int(idx + 1),
        'feature': row['feature'],
        'importance': float(row['importance']),
        'description': feature_dict[row['feature']]['description'],
        'original_feature': feature_dict[row['feature']]['original_feature']
    })

with open(os.path.join(MODELS_DIR, 'feature_importance_web.json'), 'w') as f:
    json.dump(feature_importance_web, f, indent=2)
print(f"✅ Importancia de características para web guardada: {os.path.join(MODELS_DIR, 'feature_importance_web.json')}")

# Guardar métricas completas
metrics_report = {
    'dataset_info': {
        'total_samples': len(data),
        'positive_class_ratio': float(sum(y) / len(y)),
        'train_test_split': '70/30',
        'stratified': True
    },
    'model_info': {
        'model_type': 'RidgeClassifierCV',
        'best_alpha': float(best_alpha),
        'calibration_method': 'sigmoid (Platt scaling)',
        'training_time_seconds': float(training_time),
        'calibration_time_seconds': float(calibration_time),
        'class_weights': {str(k): float(v) for k, v in class_weight_dict.items()}
    },
    'threshold_optimization': {
        'search_range': [0.1, 0.9],
        'step': 0.01,
        'best_threshold': float(best_threshold),
        'best_f1_train': float(best_f1)
    },
    'evaluation_metrics': {
        'default_threshold_0.5': {k: float(v) for k, v in metrics_default.items()},
        'optimized_threshold': {
            'threshold': float(best_threshold),
            **{k: float(v) for k, v in metrics_opt.items()}
        }
    },
    'feature_importance_top10': feature_importance.head(10).to_dict('records')
}

with open(os.path.join(MODELS_DIR, 'metrics_report.json'), 'w') as f:
    json.dump(metrics_report, f, indent=2)
print(f"✅ Reporte de métricas completo guardado: {os.path.join(MODELS_DIR, 'metrics_report.json')}")

# Resumen final
print("\n" + "=" * 80)
print("✅ RESUMEN FINAL DEL MODELADO")
print("=" * 80)
print(f"Modelo seleccionado: RidgeClassifierCV (preprocesamiento 'arboles')")
print(f"Mejor alpha: {best_alpha:.6f}")
print(f"Pesos de clase: {class_weight_dict}")
print(f"Mejor umbral de decisión: {best_threshold:.3f}")
print(f"Tiempo de entrenamiento: {training_time:.2f} segundos")
print(f"Tiempo de calibración: {calibration_time:.2f} segundos")
print("\nMétricas principales en conjunto de prueba (umbral optimizado):")
print(f"   - Accuracy:  {metrics_opt['Accuracy']:.4f}")
print(f"   - Precision: {metrics_opt['Precision']:.4f}")
print(f"   - Recall:    {metrics_opt['Recall']:.4f}")
print(f"   - F1-Score:  {metrics_opt['F1']:.4f}")
print(f"   - ROC-AUC:   {metrics_opt['ROC-AUC']:.4f}")
print(f"   - PR-AUC:    {metrics_opt['PR-AUC']:.4f}")
print("\n📈 Gráficas generadas y guardadas en:")
print(f"   - {PLOTS_DIR}")
print("\n💾 Artefactos para producción guardados en:")
print(f"   - {MODELS_DIR}")
print("\n🚀 ¡Modelo listo para integración con aplicación web!")
print("=" * 80)

# Mensaje final para la web app
print("\n💡 INSTRUCCIONES PARA LA APLICACIÓN WEB:")
print(f"- Usar el umbral optimizado: {best_threshold:.3f}")
print("- El modelo está calibrado para probabilidades fiables")
print("- Para predecir nuevos casos:")
print("  1. Aplicar el mismo preprocesamiento que data_preprocesada_arboles.csv")
print("  2. Usar el scaler guardado para escalar las características")
print("  3. Aplicar el modelo calibrado para obtener probabilidades")
print("  4. Aplicar el umbral optimizado para obtener la clasificación final")