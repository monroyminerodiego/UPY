# lazy_model_selector.py
import os
import pandas as pd
import numpy as np
from lazypredict.Supervised import LazyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings("ignore")

def load_preprocessed_data(location_path, tipo_procesamiento):
    """Carga el CSV preprocesado. Asegura que todas las columnas sean numéricas."""
    file_path = os.path.join(location_path, 'Data', 'processed', f'data_preprocesada_{tipo_procesamiento}.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró: {file_path}")
    
    df = pd.read_csv(file_path)
    if 'target' not in df.columns:
        raise ValueError(f"Columna 'target' no encontrada en {file_path}")

    # === Verificación crítica: que no haya strings ===
    non_numeric = df.drop(columns=['target']).select_dtypes(exclude=[np.number]).columns
    if len(non_numeric) > 0:
        raise TypeError(f"❌ Columnas no numéricas detectadas en '{tipo_procesamiento}': {list(non_numeric)}\n"
                        "Asegúrate de que tu preprocesador aplica one-hot/target encoding a TODAS las categóricas.")
    
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def benchmark_models_on_preprocessed_data(location_path, test_size=0.3, random_state=42):
    """
    Aplica LazyClassifier a cada tipo de dataset preprocesado y compara el mejor modelo de cada flujo.
    Retorna un ranking global por métrica (ej: 'Accuracy', 'ROC AUC', 'Recall').
    """
    tipos = ['reg_logistica', 'arboles', 'ensamble', 'red_neuronal']
    global_ranking = []  # (tipo, mejor_modelo_nombre, métricas_dict, modelo_obj)

    print("🚀 Iniciando benchmark automático con LazyPredict (LazyClassifier)...\n")
    
    for tipo in tipos:
        print(f"🔍 Analizando flujo: '{tipo}'")
        try:
            X, y = load_preprocessed_data(location_path, tipo)
            print(f"   → Shape: {X.shape} | Clase positiva (good): {y.mean():.1%}")
            
            # Hold-out split (LazyPredict usa esto por defecto: 70/30)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, stratify=y, random_state=random_state
            )

            # ⚡ Ejecutar LazyClassifier
            clf = LazyClassifier(
                verbose=0, 
                ignore_warnings=True, 
                custom_metric=None,
                predictions=False,  # Solo métricas, no guardar predicciones
                random_state=random_state
            )
            models, predictions = clf.fit(X_train, X_test, y_train, y_test)

            # El DataFrame `models` tiene columnas: Accuracy, Balanced Accuracy, ROC AUC, F1 Score, etc.
            if models.empty:
                print(f"   ✖️ Ningún modelo pudo entrenarse para '{tipo}'")
                continue

            # Agregar columna de tipo de preprocesamiento
            models['tipo_preproc'] = tipo
            models['Model'] = models.index

            # Guardar mejor modelo (por ROC AUC, y fallback a F1 si no existe)
            sort_by = 'ROC AUC' if 'ROC AUC' in models.columns else 'F1 Score'
            best_model_row = models.sort_values(by=sort_by, ascending=False).iloc[0]
            best_model_name = best_model_row.name

            # Recuperar el modelo entrenado (lazypredict no lo devuelve directamente; necesitamos reproducirlo)
            # Pero sí guardamos sus métricas y nombre.
            global_ranking.append({
                'tipo_preproc': tipo,
                'mejor_modelo': best_model_name,
                'ROC AUC': best_model_row.get('ROC AUC', np.nan),
                'Accuracy': best_model_row['Accuracy'],
                'Balanced Accuracy': best_model_row['Balanced Accuracy'],
                'F1 Score': best_model_row['F1 Score'],
                'Recall': best_model_row.get('Recall', np.nan),
                'Precision': best_model_row.get('Precision', np.nan),
                'Time Taken': best_model_row['Time Taken'],
                'model_details': best_model_row.to_dict()
            })

            print(f"   ✅ Top 3 modelos para '{tipo}':")
            top3 = models.sort_values(by=sort_by, ascending=False).head(3)
            for i, (_, row) in enumerate(top3.iterrows(), 1):
                auc = row.get('ROC AUC', 'N/A')
                f1 = row['F1 Score']
                acc = row['Accuracy']
                print(f"      {i}. {row.name:25} | AUC: {auc:>5} | F1: {f1:.3f} | Acc: {acc:.3f} | Time: {row['Time Taken']:.2f}s")

        except Exception as e:
            print(f"   ❌ Error en '{tipo}': {e}")
            import traceback
            traceback.print_exc()

    if not global_ranking:
        raise RuntimeError("Ningún flujo produjo resultados válidos.")

    # Convertir a DataFrame y ordenar globalmente por ROC AUC (o métrica principal)
    ranking_df = pd.DataFrame(global_ranking)
    
    # Priorizar métricas en orden de preferencia
    sort_metric = 'ROC AUC' if 'ROC AUC' in ranking_df.columns else 'F1 Score'
    ranking_df = ranking_df.sort_values(by=sort_metric, ascending=False).reset_index(drop=True)

    print(f"\n🏆 Ranking GLOBAL por {sort_metric}:")
    print("="*80)
    for i, row in ranking_df.iterrows():
        print(f"{i+1}. [{row['tipo_preproc']:12}] → {row['mejor_modelo']:25} | "
              f"AUC: {row['ROC AUC'] if pd.notna(row['ROC AUC']) else '—':>6} | "
              f"F1: {row['F1 Score']:.3f} | Recall: {row['Recall'] if pd.notna(row['Recall']) else '—':>5} | "
              f"{row['Time Taken']:.2f}s")

    return ranking_df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--location_path', default=os.path.dirname(os.path.dirname(__file__)),
                        help='Ruta base del proyecto (donde está la carpeta Data/)')
    args = parser.parse_args()

    try:
        ranking = benchmark_models_on_preprocessed_data(args.location_path)
        
        # Guardar ranking completo como CSV
        output_path = os.path.join(args.location_path, 'Docs', 'lazy_benchmark_ranking.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        ranking.to_csv(output_path, index=False)
        print(f"\n✅ Ranking guardado en: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()