# lazy_model_selector.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    average_precision_score,  # Esto es PR AUC
    precision_recall_curve,
    roc_auc_score,
    f1_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score
)
from lazypredict.Supervised import CLASSIFIERS, LazyClassifier
import warnings
warnings.filterwarnings("ignore")

def clean_column_names(df):
    """Limpia los nombres de columnas para eliminar caracteres problemáticos"""
    df = df.copy()
    # Reemplazar espacios, guiones y otros caracteres problemáticos
    df.columns = [col.replace(' ', '_').replace('-', '_').replace('/', '_')
                  .replace('(', '').replace(')', '').replace('<', 'less')
                  .replace('>', 'greater').replace('%', 'pct')
                  .replace('.', '_').replace(',', '_') for col in df.columns]
    # Eliminar caracteres no alfanuméricos excepto guiones bajos
    df.columns = [''.join(c if c.isalnum() or c == '_' else '_' for c in col) for col in df.columns]
    # Asegurar que no haya nombres de columna duplicados
    seen = {}
    new_columns = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_columns.append(col)
    df.columns = new_columns
    return df

def load_preprocessed_data(location_path, tipo_procesamiento):
    """Carga el CSV preprocesado y limpia los nombres de columnas"""
    file_path = os.path.join(location_path, 'Data', 'processed', f'data_preprocesada_{tipo_procesamiento}.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró: {file_path}")
    
    df = pd.read_csv(file_path)
    
    if 'target' not in df.columns:
        raise ValueError(f"Columna 'target' no encontrada en {file_path}")
    
    # Limpieza de nombres de columnas
    df = clean_column_names(df)
    
    # Verificación de que todas las columnas sean numéricas
    non_numeric = df.drop(columns=['target']).select_dtypes(exclude=[np.number]).columns
    if len(non_numeric) > 0:
        print(f"Advertencia: Columnas no numéricas detectadas en '{tipo_procesamiento}': {list(non_numeric)}")
        print("Aplicando one-hot encoding a estas columnas...")
        df = pd.get_dummies(df, columns=non_numeric, drop_first=True)
    
    # Asegurar que target sea binario (0/1)
    if not set(df['target'].unique()).issubset({0, 1}):
        print(f"Advertencia: target contiene valores no binarios: {df['target'].unique()}")
        # Si hay valores como 1 y 2, mapear 1->1 (good), 2->0 (bad)
        if set(df['target'].unique()) == {1, 2}:
            df['target'] = df['target'].map({1: 1, 2: 0})
        elif set(df['target'].unique()) == {'good', 'bad'}:
            df['target'] = df['target'].map({'good': 1, 'bad': 0})
        else:
            raise ValueError(f"Valores inesperados en target: {df['target'].unique()}")
    
    X = df.drop(columns=['target'])
    y = df['target'].astype(int)
    
    return X, y

def fit_and_get_proba(model, X_train, y_train, X_test):
    """Entrena un modelo y obtiene probabilidades de la clase positiva"""
    try:
        model.fit(X_train, y_train)
        
        # Obtener probabilidades
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)
            # Asegurar que devuelva probabilidades para la clase positiva (índice 1)
            if y_proba.shape[1] > 1:
                return y_proba[:, 1]
            else:
                return y_proba[:, 0]
        elif hasattr(model, "decision_function"):
            # Para modelos como SVM sin predict_proba
            decision = model.decision_function(X_test)
            # Convertir a probabilidades aproximadas usando sigmoide
            return 1 / (1 + np.exp(-decision))
        else:
            # Si no hay forma de obtener probabilidades, usar predicciones binarias
            y_pred = model.predict(X_test)
            return y_pred  # No es ideal, pero mejor que nada
    except Exception as e:
        print(f"  ⚠️ Error al entrenar {type(model).__name__}: {e}")
        return None

def calculate_pr_auc(y_true, y_proba):
    """Calcula Precision-Recall AUC (PR AUC)"""
    if y_proba is None or len(np.unique(y_true)) < 2:
        return np.nan
    
    try:
        return average_precision_score(y_true, y_proba)
    except Exception as e:
        print(f"  ⚠️ Error al calcular PR AUC: {e}")
        return np.nan

def benchmark_models_on_preprocessed_data(location_path, test_size=0.3, random_state=42):
    """
    Aplica LazyClassifier modificado para calcular correctamente PR AUC
    """
    tipos = ['reg_logistica', 'arboles', 'ensamble', 'red_neuronal']
    global_ranking = []
    detailed_results = {}
    
    print("🚀 Iniciando benchmark automático con LazyPredict (enfocado en PR AUC)...\n")
    
    for tipo in tipos:
        print(f"🔍 Analizando flujo: '{tipo}'")
        try:
            X, y = load_preprocessed_data(location_path, tipo)
            print(f"   → Shape: {X.shape} | Clase positiva (good): {y.mean():.1%}")
            
            # Hold-out split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, stratify=y, random_state=random_state
            )
            
            # Obtener los modelos disponibles en LazyPredict
            models_to_test = []
            for name, classifier in CLASSIFIERS:
                try:
                    # Crear instancia del modelo
                    if name in ['XGBClassifier', 'LGBMClassifier', 'CatBoostClassifier']:
                        model = classifier(random_state=random_state, verbosity=0)
                    elif name in ['SVC', 'NuSVC']:
                        model = classifier(probability=True, random_state=random_state)
                    else:
                        # Manejar modelos que no aceptan random_state
                        try:
                            model = classifier(random_state=random_state)
                        except TypeError:
                            # Algunos modelos no aceptan random_state
                            model = classifier()
                    models_to_test.append((name, model))
                except Exception as e:
                    print(f"   ⚠️ No se pudo inicializar {name}: {e}")
                    continue
            
            print(f"   ⏳ Entrenando {len(models_to_test)} modelos y calculando PR AUC...")
            
            results = []
            for name, model in models_to_test:
                try:
                    start_time = pd.Timestamp.now()
                    
                    # Entrenar modelo y obtener probabilidades
                    y_proba = fit_and_get_proba(model, X_train, y_train, X_test)
                    
                    # Obtener predicciones binarias
                    if hasattr(model, "predict"):
                        y_pred = model.predict(X_test)
                    else:
                        y_pred = (y_proba > 0.5).astype(int)
                    
                    end_time = pd.Timestamp.now()
                    elapsed_time = (end_time - start_time).total_seconds()
                    
                    # Calcular métricas
                    acc = accuracy_score(y_test, y_pred)
                    bal_acc = balanced_accuracy_score(y_test, y_pred)
                    f1 = f1_score(y_test, y_pred, zero_division=0)
                    prec = precision_score(y_test, y_pred, zero_division=0)
                    rec = recall_score(y_test, y_pred, zero_division=0)
                    
                    roc_auc = np.nan
                    pr_auc = np.nan
                    
                    if y_proba is not None:
                        try:
                            roc_auc = roc_auc_score(y_test, y_proba)
                        except:
                            pass
                        pr_auc = calculate_pr_auc(y_test, y_proba)
                    
                    # Guardar resultados
                    results.append({
                        'Model': name,
                        'Accuracy': acc,
                        'Balanced Accuracy': bal_acc,
                        'ROC AUC': roc_auc,
                        'PR AUC': pr_auc,
                        'F1 Score': f1,
                        'Precision': prec,
                        'Recall': rec,
                        'Time Taken': elapsed_time
                    })
                    
                    if pr_auc is not None and not np.isnan(pr_auc):
                        print(f"      ✅ {name:25} | PR AUC: {pr_auc:.3f} | F1: {f1:.3f} | Time: {elapsed_time:.2f}s")
                    else:
                        print(f"      ⚠️  {name:25} | PR AUC: N/A   | F1: {f1:.3f} | Time: {elapsed_time:.2f}s")
                        
                except Exception as e:
                    print(f"      ❌ {name:25} | Error: {e}")
                    continue
            
            if not results:
                print(f"   ✖️ Ningún modelo pudo entrenarse para '{tipo}'")
                continue
            
            # Convertir resultados a DataFrame
            models_df = pd.DataFrame(results).set_index('Model')
            
            # Agregar columna de tipo de preprocesamiento
            models_df['tipo_preproc'] = tipo
            
            # Guardar resultados detallados
            detailed_results[tipo] = models_df.copy()
            
            # Obtener mejor modelo por PR AUC
            valid_models = models_df[~models_df['PR AUC'].isna()]
            if len(valid_models) > 0:
                best_model_row = valid_models.sort_values(by='PR AUC', ascending=False).iloc[0]
                sort_metric = 'PR AUC'
            else:
                # Fallback a F1 Score si no hay PR AUC válido
                best_model_row = models_df.sort_values(by='F1 Score', ascending=False).iloc[0]
                sort_metric = 'F1 Score'
            
            best_model_name = best_model_row.name
            
            # Guardar información del mejor modelo
            global_ranking.append({
                'tipo_preproc': tipo,
                'mejor_modelo': best_model_name,
                'PR AUC': best_model_row.get('PR AUC', np.nan),
                'ROC AUC': best_model_row.get('ROC AUC', np.nan),
                'Accuracy': best_model_row['Accuracy'],
                'Balanced Accuracy': best_model_row['Balanced Accuracy'],
                'F1 Score': best_model_row['F1 Score'],
                'Recall': best_model_row.get('Recall', np.nan),
                'Precision': best_model_row.get('Precision', np.nan),
                'Time Taken': best_model_row['Time Taken'],
                'model_details': best_model_row.to_dict()
            })
            
            # Mostrar top 3 modelos
            top3 = models_df.sort_values(by='PR AUC', ascending=False).head(3)
            print(f"\n   ✅ Top 3 modelos para '{tipo}' (ordenados por PR AUC):")
            for i, (_, row) in enumerate(top3.iterrows(), 1):
                pr_auc_val = f"{row['PR AUC']:.3f}" if pd.notna(row['PR AUC']) else "N/A"
                print(f"      {i}. {row.name:25} | PR AUC: {pr_auc_val:>6} | F1: {row['F1 Score']:.3f} | "
                      f"Acc: {row['Accuracy']:.3f} | Time: {row['Time Taken']:.2f}s")

        except Exception as e:
            print(f"   ❌ Error en '{tipo}': {e}")
            import traceback
            traceback.print_exc()
    
    if not global_ranking:
        raise RuntimeError("Ningún flujo produjo resultados válidos.")
    
    # Convertir a DataFrame y ordenar globalmente por PR AUC
    ranking_df = pd.DataFrame(global_ranking)
    
    # Determinar métrica de ordenamiento
    if 'PR AUC' in ranking_df.columns and not ranking_df['PR AUC'].isna().all():
        sort_metric = 'PR AUC'
        ranking_df = ranking_df.sort_values(by=sort_metric, ascending=False)
    else:
        sort_metric = 'F1 Score' if 'F1 Score' in ranking_df.columns else 'Accuracy'
        ranking_df = ranking_df.sort_values(by=sort_metric, ascending=False)
    
    ranking_df = ranking_df.reset_index(drop=True)
    
    print(f"\n🏆 Ranking GLOBAL por {sort_metric}:")
    print("="*100)
    for i, row in ranking_df.iterrows():
        pr_auc_val = f"{row['PR AUC']:.3f}" if pd.notna(row['PR AUC']) else "—"
        print(f"{i+1}. [{row['tipo_preproc']:12}] → {row['mejor_modelo']:25} | "
              f"PR AUC: {pr_auc_val:>6} | F1: {row['F1 Score']:.3f} | "
              f"Recall: {row['Recall']:.3f} | Prec: {row['Precision']:.3f} | "
              f"{row['Time Taken']:.2f}s")
    
    # Guardar resultados detallados
    return ranking_df, detailed_results, (X_train, X_test, y_train, y_test)

def plot_pr_curves(location_path, detailed_results, data_splits, random_state=42):
    """Genera gráficas de las curvas Precision-Recall para los mejores modelos"""
    print("\n📊 Generando visualizaciones de curvas Precision-Recall...")
    
    os.makedirs(os.path.join(location_path, 'Docs', 'plots'), exist_ok=True)
    X_train, X_test, y_train, y_test = data_splits
    
    for tipo, models_df in detailed_results.items():
        if models_df.empty:
            continue
        
        # Obtener top 3 modelos por PR AUC
        valid_models = models_df[~models_df['PR AUC'].isna()]
        if len(valid_models) == 0:
            continue
        
        top_models = valid_models.sort_values(by='PR AUC', ascending=False).head(3).index.tolist()
        
        # Cargar datos para este tipo de preprocesamiento
        X, y = load_preprocessed_data(location_path, tipo)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=random_state
        )
        
        plt.figure(figsize=(10, 8))
        
        # Curva para cada modelo
        for model_name in top_models:
            try:
                # Encontrar la clase del modelo
                model_class = None
                for name, clf in CLASSIFIERS:
                    if name == model_name:
                        model_class = clf
                        break
                
                if model_class is None:
                    continue
                
                # Inicializar y entrenar el modelo
                if model_name in ['XGBClassifier', 'LGBMClassifier', 'CatBoostClassifier']:
                    model = model_class(random_state=random_state, verbosity=0)
                elif model_name in ['SVC', 'NuSVC']:
                    model = model_class(probability=True, random_state=random_state)
                else:
                    try:
                        model = model_class(random_state=random_state)
                    except TypeError:
                        model = model_class()
                
                # Entrenar y obtener probabilidades
                model.fit(X_train, y_train)
                
                if hasattr(model, "predict_proba"):
                    y_proba = model.predict_proba(X_test)[:, 1]
                elif hasattr(model, "decision_function"):
                    y_proba = model.decision_function(X_test)
                    y_proba = 1 / (1 + np.exp(-y_proba))  # Convertir a probabilidades
                else:
                    continue
                
                # Calcular curva PR
                precision, recall, _ = precision_recall_curve(y_test, y_proba)
                pr_auc = average_precision_score(y_test, y_proba)
                
                plt.plot(recall, precision, 
                         label=f'{model_name} (PR AUC = {pr_auc:.3f})',
                         linewidth=2)
            except Exception as e:
                print(f"   ⚠️ Error al generar curva PR para {model_name} en {tipo}: {e}")
                continue
        
        # Línea de referencia (ratio de positivos)
        plt.axhline(y=y_test.mean(), color='r', linestyle='--', 
                   label=f'Ratio positivos ({y_test.mean():.3f})')
        
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title(f'Curvas Precision-Recall - {tipo.replace("_", " ").title()}', fontsize=14)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        
        # Guardar la figura
        plot_path = os.path.join(location_path, 'Docs', 'plots', f'pr_curve_{tipo}.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Curva PR guardada para '{tipo}': {plot_path}")
    
    # Generar gráfico de comparación global
    plt.figure(figsize=(12, 8))
    
    colors = plt.cm.tab10(np.linspace(0, 1, min(10, len(detailed_results))))
    color_idx = 0
    
    for tipo, models_df in detailed_results.items():
        if models_df.empty:
            continue
        
        # Obtener mejor modelo con PR AUC válido
        valid_models = models_df[~models_df['PR AUC'].isna()]
        if len(valid_models) == 0:
            continue
        
        best_model_row = valid_models.sort_values(by='PR AUC', ascending=False).iloc[0]
        best_model_name = best_model_row.name
        
        try:
            # Cargar datos y entrenar modelo
            X, y = load_preprocessed_data(location_path, tipo)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, stratify=y, random_state=random_state
            )
            
            # Encontrar la clase del modelo
            model_class = None
            for name, clf in CLASSIFIERS:
                if name == best_model_name:
                    model_class = clf
                    break
            
            if model_class is None:
                continue
            
            # Inicializar y entrenar el modelo
            if best_model_name in ['XGBClassifier', 'LGBMClassifier', 'CatBoostClassifier']:
                model = model_class(random_state=random_state, verbosity=0)
            elif best_model_name in ['SVC', 'NuSVC']:
                model = model_class(probability=True, random_state=random_state)
            else:
                try:
                    model = model_class(random_state=random_state)
                except TypeError:
                    model = model_class()
            
            model.fit(X_train, y_train)
            
            # Obtener probabilidades
            if hasattr(model, "predict_proba"):
                y_proba = model.predict_proba(X_test)[:, 1]
            elif hasattr(model, "decision_function"):
                y_proba = model.decision_function(X_test)
                y_proba = 1 / (1 + np.exp(-y_proba))
            else:
                continue
            
            # Calcular curva PR
            precision, recall, _ = precision_recall_curve(y_test, y_proba)
            pr_auc = average_precision_score(y_test, y_proba)
            
            plt.plot(recall, precision, color=colors[color_idx],
                     label=f'{tipo.replace("_", " ")} - {best_model_name} (PR AUC={pr_auc:.3f})',
                     linewidth=2.5)
            color_idx += 1
            
        except Exception as e:
            print(f"   ⚠️ Error en comparación global para {tipo}: {e}")
            continue
    
    if color_idx > 0:
        plt.axhline(y=y_test.mean(), color='k', linestyle='--', 
                    label=f'Ratio positivos ({y_test.mean():.3f})')
        
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title('Comparación Global de Curvas Precision-Recall', fontsize=14)
        plt.legend(loc='best', fontsize=9)
        plt.grid(True, alpha=0.3)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        
        global_plot_path = os.path.join(location_path, 'Docs', 'plots', 'pr_curve_global_comparison.png')
        plt.savefig(global_plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico de comparación global guardado: {global_plot_path}")

def generate_report(location_path, ranking_df, detailed_results):
    """Genera un reporte detallado en formato CSV y resumen en consola"""
    print("\n📝 Generando reporte detallado...")
    
    # Guardar ranking global
    output_path = os.path.join(location_path, 'Docs', 'lazy_benchmark_ranking_PR_AUC.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ranking_df.to_csv(output_path, index=False)
    print(f"✅ Ranking global guardado en: {output_path}")
    
    # Guardar resultados detallados por tipo de preprocesamiento
    for tipo, models_df in detailed_results.items():
        if not models_df.empty:
            detailed_path = os.path.join(location_path, 'Docs', f'lazy_results_{tipo}.csv')
            models_df.to_csv(detailed_path)
            print(f"✅ Resultados detallados para '{tipo}' guardados en: {detailed_path}")
    
    # Generar resumen en consola
    print("\n" + "="*80)
    print("RESUMEN EJECUTIVO - MEJORES MODELOS POR TIPO DE PREPROCESAMIENTO")
    print("="*80)
    
    for tipo in ['reg_logistica', 'arboles', 'ensamble', 'red_neuronal']:
        if tipo in detailed_results and not detailed_results[tipo].empty:
            df = detailed_results[tipo]
            valid_models = df[~df['PR AUC'].isna()]
            if len(valid_models) > 0:
                best_model = valid_models.sort_values(by='PR AUC', ascending=False).iloc[0]
                print(f"\n{tipo.replace('_', ' ').title()}:")
                print(f"  Mejor modelo: {best_model.name}")
                print(f"  PR AUC: {best_model['PR AUC']:.4f}")
                print(f"  F1 Score: {best_model['F1 Score']:.4f}")
                print(f"  Tiempo de entrenamiento: {best_model['Time Taken']:.2f}s")
            else:
                print(f"\n{tipo.replace('_', ' ').title()}:")
                print("  No se pudo calcular PR AUC para ningún modelo")
    
    print("\n" + "="*80)
    print("CONCLUSIONES Y RECOMENDACIONES")
    print("="*80)
    
    # Filtrar solo modelos con PR AUC válido
    valid_ranking = ranking_df[~ranking_df['PR AUC'].isna()]
    if len(valid_ranking) > 0:
        best_overall = valid_ranking.iloc[0]
        print(f"🏆 MEJOR MODELO GLOBAL (por PR AUC):")
        print(f"   Tipo de preprocesamiento: {best_overall['tipo_preproc']}")
        print(f"   Modelo: {best_overall['mejor_modelo']}")
        print(f"   PR AUC: {best_overall['PR AUC']:.4f}")
        print(f"   F1 Score: {best_overall['F1 Score']:.4f}")
        print(f"   Tiempo de entrenamiento: {best_overall['Time Taken']:.2f}s")
        
        print(f"\n💡 RECOMENDACIÓN:")
        print(f"   Utilizar el preprocesamiento '{best_overall['tipo_preproc']}' con el modelo '{best_overall['mejor_modelo']}'")
        print(f"   para maximizar el rendimiento en la detección de clientes buenos (clase positiva).")
        
        if best_overall['tipo_preproc'] == 'red_neuronal':
            print("\n   ⚠️ NOTA: Modelos de redes neuronales pueden requerir más recursos computacionales")
        elif best_overall['tipo_preproc'] == 'ensamble':
            print("\n   ⚠️ NOTA: Modelos ensemble suelen ser más lentos en predicción pero más precisos")
    else:
        print("❌ NO SE ENCONTRÓ NINGÚN MODELO CON PR AUC VÁLIDO")
        print("   Revisar el preprocesamiento de datos y las características de los modelos")

if __name__ == "__main__":
    import argparse
    
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Benchmark automático de modelos ML con enfoque en PR AUC')
    parser.add_argument('--location_path', 
                        default=os.path.dirname(os.path.dirname(__file__)),
                        help='Ruta base del proyecto (donde está la carpeta Data/)')
    parser.add_argument('--test_size', type=float, default=0.3,
                        help='Tamaño del conjunto de prueba (default: 0.3)')
    parser.add_argument('--random_state', type=int, default=42,
                        help='Semilla para reproducibilidad (default: 42)')
    parser.add_argument('--no_plots', action='store_true',
                        help='No generar gráficas de curvas PR')
    
    args = parser.parse_args()
    
    try:
        print(f"📍 Ruta del proyecto: {args.location_path}")
        print(f"⚙️  Parámetros: test_size={args.test_size}, random_state={args.random_state}")
        
        # Ejecutar benchmark
        ranking_df, detailed_results, data_splits = benchmark_models_on_preprocessed_data(
            location_path=args.location_path,
            test_size=args.test_size,
            random_state=args.random_state
        )
        
        # Generar gráficas si no se desactivaron
        if not args.no_plots:
            plot_pr_curves(args.location_path, detailed_results, data_splits, args.random_state)
        
        # Generar reporte
        generate_report(args.location_path, ranking_df, detailed_results)
        
        print(f"\n🎉 ¡Benchmark completado exitosamente!")
        print(f"📂 Resultados guardados en: {os.path.join(args.location_path, 'Docs')}")
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()