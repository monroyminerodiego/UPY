import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
from lazypredict.Supervised import LazyClassifier
import warnings
warnings.filterwarnings('ignore')

def load_and_evaluate_preprocessing(preprocessing_type):
    """Carga y evalúa un tipo específico de preprocesamiento"""
    print(f"\n{'='*60}")
    print(f"EVALUANDO PREPROCESAMIENTO: {preprocessing_type.upper()}")
    print(f"{'='*60}")
    
    try:
        # Cargar datos preprocesados
        file_path = f"Data/processed/data_preprocesada_{preprocessing_type}.csv"
        df = pd.read_csv(file_path)
        print(f"✓ Dataset cargado: {df.shape}")
        
        # Separar características y target
        X = df.drop('target', axis=1)
        y = df['target']
        
        print(f"✓ Características: {X.shape[1]}, Target: {y.shape[0]}")
        print(f"✓ Distribución del target: {y.value_counts().to_dict()}")
        
        # División estratificada
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=0.2, 
            stratify=y, 
            random_state=42
        )
        
        print(f"✓ Conjunto de entrenamiento: {X_train.shape}")
        print(f"✓ Conjunto de prueba: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test, preprocessing_type
        
    except Exception as e:
        print(f"✗ Error cargando {preprocessing_type}: {e}")
        return None, None, None, None, preprocessing_type

def get_best_model_with_proba(lazy_clf, models_df):
    """Selecciona el mejor modelo que tenga predict_proba"""
    proba_models = []
    
    for model_name, model in lazy_clf.models.items():
        try:
            # Verificar si el modelo tiene predict_proba
            if hasattr(model, 'predict_proba'):
                # Probar llamar a predict_proba en una pequeña muestra
                if hasattr(model, 'steps'):  # Si es un pipeline
                    proba_models.append(model_name)
                else:
                    # Para modelos individuales
                    proba_models.append(model_name)
        except:
            continue
    
    print(f"✓ Modelos con predict_proba disponibles: {len(proba_models)}")
    
    # Filtrar el dataframe para solo modelos con predict_proba
    proba_models_df = models_df[models_df.index.isin(proba_models)]
    
    if len(proba_models_df) == 0:
        return None, None
    
    # Seleccionar el mejor por Balanced Accuracy
    best_model_name = proba_models_df.nlargest(1, 'Balanced Accuracy').index[0]
    best_model = lazy_clf.models[best_model_name]
    
    return best_model, best_model_name

def evaluate_focused_metrics(model, X_test, y_test, preprocessing_type):
    """Evalúa métricas enfocadas en detectar malos pagadores"""
    print(f"\n📊 EVALUACIÓN ESPECÍFICA PARA {preprocessing_type.upper()}")
    
    try:
        # Predicciones
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Para modelos de sklearn, las clases están ordenadas, clase 0 es la primera
        # Verificar el orden de las clases
        if hasattr(model, 'classes_'):
            class_order = model.classes_
            if class_order[0] == 0:  # Malos pagadores son clase 0
                y_pred_proba_malos = y_pred_proba[:, 0]
            else:
                y_pred_proba_malos = y_pred_proba[:, 1]
        else:
            # Asumir que la primera columna es clase 0 (malos pagadores)
            y_pred_proba_malos = y_pred_proba[:, 0]
        
        # Métricas básicas
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        # Asegurar que la matriz de confusión se interpreta correctamente
        # Clase 0: malos pagadores, Clase 1: buenos pagadores
        tn, fp, fn, tp = cm.ravel()
        
        # MÉTRICAS ESPECÍFICAS PARA MALOS PAGADORES (Clase 0)
        # Sensitivity/Recall para clase 0: TN / (TN + FP)
        sensitivity_0 = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        # Precision para clase 0: TN / (TN + FN)  
        precision_0 = tn / (tn + fn) if (tn + fn) > 0 else 0
        
        # F1-score para clase 0
        f1_0 = 2 * (precision_0 * sensitivity_0) / (precision_0 + sensitivity_0) if (precision_0 + sensitivity_0) > 0 else 0
        
        # AUC-ROC
        auc_roc = roc_auc_score(y_test, y_pred_proba_malos)
        
        # AUC-PR (Precision-Recall) - mejor para clases desbalanceadas
        precision, recall, _ = precision_recall_curve(y_test, y_pred_proba_malos, pos_label=0)
        auc_pr = -np.trapz(precision, recall) if len(precision) > 1 else 0
        
        print(f"🎯 MÉTRICAS PARA MALOS PAGADORES (Clase 0):")
        print(f"   • Sensitivity/Recall: {sensitivity_0:.4f} (capacidad de detectar malos pagadores)")
        print(f"   • Precision: {precision_0:.4f} (cuán precisos son los que marcamos como malos)")
        print(f"   • F1-Score: {f1_0:.4f}")
        print(f"   • AUC-ROC: {auc_roc:.4f}")
        print(f"   • AUC-PR: {auc_pr:.4f} (mejor métrica para clases desbalanceadas)")
        print(f"   • Matriz de confusión:")
        print(f"                 Predicción")
        print(f"               Malo   Bueno")
        print(f"Real Malo    [{tn:3d}    {fp:3d}]")
        print(f"Real Bueno   [{fn:3d}    {tp:3d}]")
        
        return {
            'preprocessing': preprocessing_type,
            'sensitivity_0': sensitivity_0,
            'precision_0': precision_0,
            'f1_0': f1_0,
            'auc_roc': auc_roc,
            'auc_pr': auc_pr,
            'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp
        }
        
    except Exception as e:
        print(f"✗ Error en evaluación específica: {e}")
        import traceback
        traceback.print_exc()
        return None

def lazy_modeling_analysis():
    """Análisis completo con LazyPredict para los 4 tipos de preprocesamiento"""
    
    preprocessing_types = ['reg_logistica', 'arboles', 'ensamble', 'red_neuronal']
    all_results = []
    
    for preproc_type in preprocessing_types:
        # Cargar datos
        X_train, X_test, y_train, y_test, preproc_name = load_and_evaluate_preprocessing(preproc_type)
        
        if X_train is None:
            continue
            
        print(f"\n🚀 ENTRENANDO CON LAZYPREDICT PARA {preproc_name.upper()}...")
        
        try:
            # Configurar LazyClassifier
            lazy_clf = LazyClassifier(
                verbose=0,
                ignore_warnings=True,
                custom_metric=None,
                random_state=42,
                classifiers='all'
            )
            
            # Entrenar y evaluar modelos
            models, predictions = lazy_clf.fit(X_train, X_test, y_train, y_test)
            
            print(f"✓ Modelos evaluados: {len(models)}")
            
            # Filtrar top 10 modelos por Balanced Accuracy
            top_models = models.nlargest(10, 'Balanced Accuracy')
            print(f"\n🏆 TOP 10 MODELOS PARA {preproc_name.upper()}:")
            print(top_models[['Balanced Accuracy', 'ROC AUC', 'F1 Score', 'Time Taken']])
            
            # Obtener el mejor modelo CON predict_proba
            best_model, best_model_name = get_best_model_with_proba(lazy_clf, models)
            
            if best_model is None:
                print(f"⚠ No se encontraron modelos con predict_proba para {preproc_name}")
                continue
            
            print(f"\n⭐ MEJOR MODELO CON predict_proba: {best_model_name}")
            
            # Evaluación específica para detección de malos pagadores
            focused_metrics = evaluate_focused_metrics(best_model, X_test, y_test, preproc_name)
            
            if focused_metrics:
                focused_metrics['best_model'] = best_model_name
                focused_metrics['balanced_accuracy'] = models.loc[best_model_name, 'Balanced Accuracy']
                all_results.append(focused_metrics)
                
        except Exception as e:
            print(f"✗ Error en LazyPredict para {preproc_type}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return all_results

def final_recommendation(results):
    """Genera recomendación final basada en todos los resultados"""
    print(f"\n{'='*80}")
    print("🎯 RECOMENDACIÓN FINAL")
    print(f"{'='*80}")
    
    if not results:
        print("No se pudieron obtener resultados válidos de ningún preprocesamiento.")
        return None
    
    # Convertir a DataFrame para análisis
    results_df = pd.DataFrame(results)
    
    # Ponderar métricas (énfasis en sensitivity y AUC-PR para detectar malos pagadores)
    results_df['weighted_score'] = (
        results_df['sensitivity_0'] * 0.35 +  # Mayor peso a sensitivity (detectar malos)
        results_df['auc_pr'] * 0.30 +         # AUC-PR muy importante para clases desbalanceadas
        results_df['auc_roc'] * 0.20 +
        results_df['f1_0'] * 0.15
    )
    
    # Mejor combinación
    best_idx = results_df['weighted_score'].idxmax()
    best_combo = results_df.loc[best_idx]
    
    print("📈 RESULTADOS COMPARATIVOS:")
    print("-" * 80)
    for idx, row in results_df.iterrows():
        print(f"{row['preprocessing'].upper():<15} | "
              f"Sens: {row['sensitivity_0']:.3f} | "
              f"AUC-PR: {row['auc_pr']:.3f} | "
              f"AUC-ROC: {row['auc_roc']:.3f} | "
              f"F1: {row['f1_0']:.3f} | "
              f"Modelo: {row['best_model']}")
    
    print(f"\n🏅 MEJOR COMBINACIÓN:")
    print(f"   • Preprocesamiento: {best_combo['preprocessing']}")
    print(f"   • Modelo: {best_combo['best_model']}")
    print(f"   • Sensitivity (detección malos pagadores): {best_combo['sensitivity_0']:.3f}")
    print(f"   • AUC-PR: {best_combo['auc_pr']:.3f}")
    print(f"   • AUC-ROC: {best_combo['auc_roc']:.3f}")
    print(f"   • F1-Score (malos pagadores): {best_combo['f1_0']:.3f}")
    print(f"   • Puntuación ponderada: {best_combo['weighted_score']:.3f}")
    
    print(f"\n💡 RECOMENDACIÓN ESTRATÉGICA:")
    print(f"   Para detectar eficientemente malos pagadores, use:")
    print(f"   → Preprocesamiento: {best_combo['preprocessing']}")
    print(f"   → Algoritmo: {best_combo['best_model']}")
    print(f"   → Este enfoque detecta correctamente el {best_combo['sensitivity_0']*100:.1f}% de los malos pagadores")
    
    # Análisis del costo/beneficio
    fn_cost = best_combo['fn']  # Malos pagadores clasificados como buenos (PÉRDIDA)
    fp_cost = best_combo['fp']  # Buenos pagadores clasificados como malos (OPORTUNIDAD PERDIDA)
    
    print(f"\n💰 ANÁLISIS DE COSTOS:")
    print(f"   • Malos pagadores no detectados (FN): {fn_cost} → PÉRDIDA DIRECTA")
    print(f"   • Buenos pagadores rechazados (FP): {fp_cost} → OPORTUNIDAD PERDIDA")
    
    # Recomendación basada en el tipo de preprocesamiento
    if 'arboles' in best_combo['preprocessing'] or 'ensamble' in best_combo['preprocessing']:
        print(f"   → Ventaja: Los modelos basados en árboles capturan mejor interacciones no lineales")
        print(f"   → Ideal para: Detectar patrones complejos en el comportamiento de pago")
    elif 'red_neuronal' in best_combo['preprocessing']:
        print(f"   → Ventaja: La red neuronal maneja bien relaciones complejas y embeddings")
        print(f"   → Ideal para: Capturar relaciones no lineales sofisticadas")
    else:
        print(f"   → Ventaja: La regresión logística ofrece buena interpretabilidad")
        print(f"   → Ideal para: Entender factores específicos que afectan el riesgo")
    
    return best_combo

if __name__ == "__main__":
    print("🤖 INICIANDO ANÁLISIS COMPARATIVO CON LAZYPREDICT")
    print("🎯 Objetivo: Encontrar la mejor combinación preprocesamiento-modelo")
    print("   para detectar malos pagadores (clase 0)")
    print("📊 Métricas clave: Sensitivity y AUC-PR (prioridad detectar malos pagadores)")
    
    # Ejecutar análisis completo
    results = lazy_modeling_analysis()
    
    # Generar recomendación final
    best_combo = final_recommendation(results)
    
    if best_combo is not None:
        print(f"\n✅ ANÁLISIS COMPLETADO - MEJOR ELECCIÓN IDENTIFICADA")
    else:
        print(f"\n❌ ANÁLISIS COMPLETADO - NO SE ENCONTRÓ COMBINACIÓN VÁLIDA")