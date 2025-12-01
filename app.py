import os, pickle, json, traceback, sys
import numpy as np, pandas as pd
from flask import Flask, render_template, send_file, abort, request, jsonify
from sklearn.decomposition import PCA

location_path = os.path.dirname(__file__)
app = Flask(
    __name__,
    template_folder = os.path.join(location_path,'Files'),
    static_folder   = os.path.join(location_path,'Files')
)

# ===== General
@app.route('/')
def index():
    
    materias_final = {}

    # ===== 9no
    materias_9 = {
        "Digital Economy":[
            "Smart Factory Data Pipeline Challenge",
            "Business Model"
        ],
        "Visualization Tools II":[
            "Personalized Web",
            "Kafka Clicker",
            "Kafka Dashboard",
        ],
        "Business Intelligence":[
            "Credit Risk",
            "BigMart Analisys"
        ]
    }
    for k,v in materias_9.items(): materias_final[k] = v
    
    # ===== 8vo
    materias_8 = {
        'English VIII': [
            "TED Talk",
        ],
        'Social Network Analysis':[
            'Friendship Paradox'
        ],
        'Visualization Tools I':[
            'Badges - Diego Monroy',
            'WikiStream Analytics',
            'Engineering Week'
        ]
    }
    for k,v in materias_8.items(): materias_final[k] = v

    materias_final = dict(sorted(materias_final.items(),key=lambda item: item[0]))

    return render_template('/index.html', materias = materias_final)


# ===== Business Intelligence
# === BigMart Endpoints
# Definimos la ruta absoluta al CSV para evitar errores de lectura
BASE_DATA_PATH = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'HW4', 'Data')
RAW_CSV_PATH = os.path.join(BASE_DATA_PATH, 'Raw', 'train.csv')

def get_eda_data():
    """Función auxiliar para cargar el dataset solo cuando se necesite"""
    try:
        if os.path.exists(RAW_CSV_PATH):
            return pd.read_csv(RAW_CSV_PATH)
        else:
            print(f"Error: No se encuentra el archivo en {RAW_CSV_PATH}")
            return None
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        return None

def get_merged_dashboard_data():
    """Helper para combinar Transacciones Raw con Clusters"""
    try:
        raw_path = os.path.join(BASE_DATA_PATH, 'Raw', 'train.csv')
        clusters_path = os.path.join(BASE_DATA_PATH, 'Processed', 'product_level_with_clusters.csv')
        
        df_trans = pd.read_csv(raw_path)
        df_clusters = pd.read_csv(clusters_path)
        
        # Merge de columnas clave
        cols_cluster = ['Item_Identifier', 'Cluster_Label', 'Broad_Category']
        df_merged = df_trans.merge(df_clusters[cols_cluster], on='Item_Identifier', how='left')
        return df_merged
    except Exception as e:
        print(f"Error merging dashboard data: {e}")
        return None

@app.route('/business-intelligence/bigmart-analisys/eda/summary')
def get_eda_summary():
    print('Se llamo a get_eda_summary')
    df = get_eda_data()
    if df is None: return jsonify({"error": "Data not found"}), 404

    # Cálculos básicos de la Fase A
    nulls_per_col = df.isnull().sum()
    nulls_filtered = nulls_per_col[nulls_per_col > 0].to_dict() # Solo enviamos las que tienen nulos
    
    summary = {
        "total_rows": int(df.shape[0]),
        "total_cols": int(df.shape[1]),
        "duplicates": int(df.duplicated().sum()),
        "missing_values": nulls_filtered, # Diccionario: {'Outlet_Size': 2410, ...}
        "numeric_vars": ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Item_Outlet_Sales'],
        "categorical_vars": ['Item_Fat_Content', 'Item_Type', 'Outlet_Size', 'Outlet_Location_Type']
    }
    return jsonify(summary)

@app.route('/business-intelligence/bigmart-analisys/eda/encoding-scaling-info')
def get_eda_encoding_scaling_info():
    """
    Documenta los métodos de encoding y scaling aplicados
    """
    print("Se llamo a get_eda_encoding_scaling_info")
    
    return jsonify({
        "encoding": {
            "method": "One-Hot Encoding",
            "applied_to": [
                "Item_Fat_Content",
                "Broad_Category"
            ],
            "rationale": "Variables nominales sin orden jerárquico requieren codificación binaria",
            "example": {
                "Item_Fat_Content_Low Fat": "1 si es Low Fat, 0 si no",
                "Item_Fat_Content_Regular": "1 si es Regular, 0 si no",
                "Item_Fat_Content_Non-Edible": "1 si es Non-Edible, 0 si no"
            }
        },
        "scaling": {
            "method": "StandardScaler (Z-score normalization)",
            "formula": "(X - μ) / σ",
            "applied_to": [
                "Total_Sales",
                "Avg_Sales", 
                "Store_Count",
                "Avg_MRP",
                "Avg_Visibility",
                "Item_Weight"
            ],
            "rationale": "K-Means es sensible a la escala de variables; estandarización evita dominancia de variables con mayor magnitud",
            "effect": "Media = 0, Desviación Estándar = 1"
        },
        "preprocessing_pipeline": [
            "1. Limpieza de datos (Fat Content, duplicados)",
            "2. Imputación de valores faltantes",
            "3. Feature Engineering (Broad_Category, Years_Established)",
            "4. One-Hot Encoding (variables categóricas)",
            "5. StandardScaler (variables numéricas)",
            "6. PCA para visualización (opcional, no usado en clustering)"
        ]
    })

@app.route('/business-intelligence/bigmart-analisys/eda/missing-values-chart')
def get_eda_missing_values_chart():
    """
    Endpoint optimizado para crear gráfica de barras de valores faltantes
    Retorna: Array de objetos con columna, cantidad y porcentaje
    """
    print("Se llamo a get_eda_missing_values_chart")
    
    df = get_eda_data()
    if df is None: 
        return jsonify({"error": "Data not found"}), 404
    
    total_rows = len(df)
    missing_data = []
    
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            missing_data.append({
                "column": col,
                "count": int(missing_count),
                "percentage": round((missing_count / total_rows) * 100, 2)
            })
    
    # Ordenar por cantidad de faltantes (mayor a menor)
    missing_data_sorted = sorted(missing_data, key=lambda x: x['count'], reverse=True)
    
    return jsonify({
        "data": missing_data_sorted,
        "total_records": int(total_rows),
        "columns_with_missing": len(missing_data_sorted)
    })

@app.route('/business-intelligence/bigmart-analisys/eda/fat-content-cleanup')
def get_eda_fat_content_cleanup():
    """
    Muestra el proceso de limpieza de Item_Fat_Content
    Retorna: Distribución ANTES y DESPUÉS de la corrección
    """
    print("Se llamo a get_eda_fat_content_cleanup")
    
    df_raw = get_eda_data()
    if df_raw is None:
        return jsonify({"error": "Data not found"}), 404
    
    # Conteo ANTES de la corrección
    before_counts = df_raw['Item_Fat_Content'].value_counts().to_dict()
    
    # Aplicar corrección (simulación de lo que hiciste en preprocessing)
    df_clean = df_raw.copy()
    df_clean['Item_Fat_Content'] = df_clean['Item_Fat_Content'].replace({
        'low fat': 'Low Fat',
        'LF': 'Low Fat',
        'reg': 'Regular'
    })
    
    # Conteo DESPUÉS de la corrección
    after_counts = df_clean['Item_Fat_Content'].value_counts().to_dict()
    
    # Calcular registros corregidos
    corrections_made = {
        "LF → Low Fat": before_counts.get('LF', 0),
        "low fat → Low Fat": before_counts.get('low fat', 0),
        "reg → Regular": before_counts.get('reg', 0)
    }
    
    total_corrections = sum(corrections_made.values())
    
    return jsonify({
        "before": {
            "labels": list(before_counts.keys()),
            "values": list(before_counts.values())
        },
        "after": {
            "labels": list(after_counts.keys()),
            "values": list(after_counts.values())
        },
        "corrections_applied": corrections_made,
        "total_records_corrected": int(total_corrections),
        "standardization_rules": [
            "LF → Low Fat",
            "low fat → Low Fat", 
            "reg → Regular"
        ]
    })

@app.route('/business-intelligence/bigmart-analisys/eda/feature-engineering')
def get_eda_feature_engineering():
    """
    Documenta el proceso de Feature Engineering aplicado
    Retorna: Ejemplos de transformaciones realizadas
    """
    print("Se llamo a get_eda_feature_engineering")
    df = get_eda_data()
    if df is None:
        return jsonify({"error": "Data not found"}), 404
    
    # 1. Broad_Category Mapping
    # Mapeo Item_Type → Broad_Category (basado en tu lógica de negocio)
    category_mapping = {
        'Dairy': 'Food',
        'Soft Drinks': 'Drinks',
        'Meat': 'Food',
        'Fruits and Vegetables': 'Food',
        'Household': 'Non-Consumable',
        'Baking Goods': 'Food',
        'Snack Foods': 'Food',
        'Frozen Foods': 'Food',
        'Breakfast': 'Food',
        'Health and Hygiene': 'Non-Consumable',
        'Hard Drinks': 'Drinks',
        'Canned': 'Food',
        'Breads': 'Food',
        'Starchy Foods': 'Food',
        'Others': 'Non-Consumable',
        'Seafood': 'Food'
    }
    
    # Aplicar mapeo
    df_sample = df[['Item_Type']].drop_duplicates().copy()
    df_sample['Broad_Category'] = df_sample['Item_Type'].map(category_mapping)
    
    broad_category_examples = df_sample.to_dict(orient='records')
    
    # 2. Years_Established Calculation
    current_year = 2013  # Año del dataset según contexto
    df_years = df[['Outlet_Identifier', 'Outlet_Establishment_Year']].drop_duplicates().copy()
    df_years['Years_Established'] = current_year - df_years['Outlet_Establishment_Year']
    
    years_examples = df_years.sort_values('Years_Established', ascending=False).head(5).to_dict(orient='records')
    
    # 3. Resumen de transformaciones
    return jsonify({
        "broad_category": {
            "description": "Agrupación de 16 tipos de productos en 3 macro-categorías",
            "mapping": category_mapping,
            "examples": broad_category_examples,
            "distribution": df['Item_Type'].map(category_mapping).value_counts().to_dict()
        },
        "years_established": {
            "description": f"Antigüedad de la tienda calculada como: {current_year} - Outlet_Establishment_Year",
            "reference_year": current_year,
            "examples": years_examples,
            "range": {
                "min": int(df_years['Years_Established'].min()),
                "max": int(df_years['Years_Established'].max()),
                "avg": round(df_years['Years_Established'].mean(), 2)
            }
        },
        "transformations_summary": [
            "Item_Type → Broad_Category (16 → 3 categorías)",
            "Outlet_Establishment_Year → Years_Established (antigüedad)",
            "Estandarización de Item_Fat_Content",
            "Imputación de Item_Weight por media de producto",
            "Imputación de Outlet_Size por moda de tipo de tienda"
        ]
    })

@app.route('/business-intelligence/bigmart-analisys/eda/distributions-numeric')
def get_eda_numeric():
    print("Se llamo a get_eda_numeric")
    df = get_eda_data()
    if df is None: return jsonify({"error": "Data not found"}), 404

    # Enviamos los datos crudos de las columnas numéricas clave para que Plotly JS haga el binning
    # Limitamos a columnas clave para no saturar la red
    cols_of_interest = ['Item_MRP', 'Item_Visibility', 'Item_Outlet_Sales', 'Item_Weight']
    
    # Manejo de nulos simple para visualización (fill con 0 o drop, aquí hacemos dropna para la gráfica)
    data = { col: df[col].dropna().tolist() for col in cols_of_interest }
    
    return jsonify(data)

@app.route('/business-intelligence/bigmart-analisys/eda/distributions-categorical')
def get_eda_categorical():
    print("Se llamo get_eda_categorical")
    df = get_eda_data()
    if df is None: return jsonify({"error": "Data not found"}), 404

    categoricals = ['Item_Fat_Content', 'Item_Type', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
    data = {}

    for col in categoricals:
        # Convertimos NaN a 'Missing' para que salga en la gráfica
        counts = df[col].fillna('Missing').value_counts()
        data[col] = {
            "labels": counts.index.tolist(),
            "values": counts.values.tolist()
        }

    return jsonify(data)

@app.route('/business-intelligence/bigmart-analisys/eda/correlations')
def get_eda_correlations():
    print("Se llamo get_eda_correlations")
    df = get_eda_data()
    if df is None: return jsonify({"error": "Data not found"}), 404

    # Seleccionar solo numéricas
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().round(2)

    data = {
        "x": corr_matrix.columns.tolist(),
        "y": corr_matrix.columns.tolist(),
        "z": corr_matrix.values.tolist()
    }
    return jsonify(data)

@app.route('/business-intelligence/bigmart-analisys/eda/process-narrative')
def get_eda_narrative():
    print("Se llamo a get_eda_narrative")
    return jsonify({
        "fat_content_fix": "Se estandarizaron valores como 'LF' y 'low fat' a 'Low Fat'.",
        "missing_values_treatment": "Item_Weight imputado con la media por producto. Outlet_Size imputado por la moda según el tipo de tienda.",
        "feature_engineering": "Creación de 'Broad_Category' para agrupar items y 'Years_Established' basado en el año de fundación.",
        "encoding_scaling": "One-Hot Encoding para variables nominales y StandardScaler para numéricas antes del PCA."
    })

@app.route('/business-intelligence/bigmart-analisys/modeling/metrics')
def get_modeling_metrics():
    print("Se llamo a get_modeling_metrics")
    data = {
        "k_values": [2, 3, 4, 5, 6, 10, 15],
        "inertia": [14103.2, 11347.1, 9413.4, 8044.4, 7234.0, 5923.2, 4940.5],
        "silhouette": [0.3156, 0.2776, 0.3109, 0.2927, 0.2927, 0.2144, 0.2116],
        "selected_k": 4,
        "decision_rationale": "K=4 was chosen because it maximizes the Silhouette (0.3109) before the drop at K=6, thus avoiding excessive fragmentation."
    }
    return jsonify(data)

@app.route('/business-intelligence/bigmart-analisys/modeling/pca')
def get_modeling_pca():
    print("Se llamo a get_modeling_pca")
    # 1. Cargar datos numéricos escalados (Features)
    df_model_path = os.path.join(BASE_DATA_PATH, 'Processed', 'product_level_modeling.csv')
    # 2. Cargar datos con etiquetas de clusters (Labels)
    df_clusters_path = os.path.join(BASE_DATA_PATH, 'Processed', 'product_level_with_clusters.csv')
    
    if not os.path.exists(df_model_path) or not os.path.exists(df_clusters_path):
        return jsonify({"error": "Modeling files not found"}), 404

    try:
        # Carga
        df_model = pd.read_csv(df_model_path)
        df_clusters = pd.read_csv(df_clusters_path)

        # Aseguramos que 'Item_Identifier' sea el índice para alinear
        if 'Item_Identifier' in df_model.columns:
            df_model.set_index('Item_Identifier', inplace=True)
        
        # PCA - Reducción a 2 componentes
        pca = PCA(n_components=2)
        pca_components = pca.fit_transform(df_model)
        
        # Crear estructura de respuesta uniendo coordenadas con etiquetas de cluster
        # Asumimos que el orden de filas se mantiene, pero usamos el index para estar seguros
        response_data = []
        
        # Alineamos usando el identificador común
        for idx, item_id in enumerate(df_model.index):
            # Buscar metadata del cluster para este item
            meta = df_clusters[df_clusters['Item_Identifier'] == item_id].iloc[0]
            
            response_data.append({
                "id": item_id,
                "x": float(pca_components[idx, 0]),
                "y": float(pca_components[idx, 1]),
                "cluster_id": int(meta['Cluster']),
                "cluster_label": meta['Cluster_Label'],
                "category": meta['Broad_Category'] # Útil para el tooltip
            })

        return jsonify({
            "explained_variance": pca.explained_variance_ratio_.tolist(),
            "data": response_data,
            "visual_discrepancy_note": "The 2D PCA visually overlaps the 'Food' clusters (Economy vs Premium) that the K-Means algorithm was able to separate in the multidimensional space."
        })

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/business-intelligence/bigmart-analisys/modeling/cluster-profiles')
def get_modeling_profiles():
    print("Se llamo a get_modeling_profiles")
    df_clusters_path = os.path.join(BASE_DATA_PATH, 'Processed', 'product_level_with_clusters.csv')
    
    if not os.path.exists(df_clusters_path):
        return jsonify({"error": "Cluster file not found"}), 404
        
    df = pd.read_csv(df_clusters_path)
    
    # Definir descripciones (Hardcoded basado en tu análisis de la Fase C)
    descriptions = {
        "Drinks": "Low margin, high rotation, medium volume.",
        "Food: Low Viz / Economy": "Basic products, low shelf visibility.",
        "Food: Mass Market / High Rev": "Traffic drivers, medium prices, high sales.",
        "Non-Edible Goods": "Cleaning and household products, stable performance."
    }
    
    profile = df.groupby('Cluster_Label')[['Total_Sales', 'Avg_MRP', 'Avg_Visibility', 'Store_Count']].mean().reset_index()
    profile = profile.round(2)
    
    # Convertir a lista de dicts y agregar descripción
    records = profile.to_dict(orient='records')
    for record in records:
        lbl = record['Cluster_Label']
        record['description'] = descriptions.get(lbl, "Sin descripción definida")
        
    return jsonify(records)

@app.route('/business-intelligence/bigmart-analisys/dashboards/store-hierarchy')
def get_dashboard_hierarchy():
    print("Se llamo a get_dashboard_hierarchy")
    json_path = os.path.join(BASE_DATA_PATH, 'Processed', 'store_hierarchy_final.json')
    if not os.path.exists(json_path):
        return jsonify({"error": "Hierarchy JSON not found"}), 404
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/dashboards/strategic-premium')
def get_dashboard_premium():
    print("Se llamo a get_dashboard_premium")
    df = get_merged_dashboard_data()
    if df is None: return jsonify({"error": "Data processing error"}), 500

    # Lógica de Price Tier (Replicando Fase D)
    quartiles = df['Item_MRP'].quantile([0.33, 0.66]).values
    
    def classify_price(mrp):
        if mrp < quartiles[0]: return 'Economy'
        elif mrp < quartiles[1]: return 'Standard'
        else: return 'Premium'

    df['Price_Tier'] = df['Item_MRP'].apply(classify_price)
    
    # Agrupación: Ventas promedio por Tipo de Tienda y Tier de Precio
    price_sensitivity = df.groupby(['Outlet_Type', 'Price_Tier'])['Item_Outlet_Sales'].mean().reset_index()
    
    # Estructuramos para fácil consumo en frontend (Nested JSON o Flat)
    result = []
    for outlet in price_sensitivity['Outlet_Type'].unique():
        subset = price_sensitivity[price_sensitivity['Outlet_Type'] == outlet]
        tiers = {row['Price_Tier']: round(row['Item_Outlet_Sales'], 2) for _, row in subset.iterrows()}
        result.append({
            "outlet_type": outlet,
            "values": tiers # Ej: {'Economy': 1500, 'Premium': 2500}
        })
        
    return jsonify(result)

@app.route('/business-intelligence/bigmart-analisys/dashboards/geo-analysis')
def get_dashboard_geo():
    print("Se llamo a get_dashboard_geo")
    df = get_merged_dashboard_data()
    if df is None: return jsonify({"error": "Data processing error"}), 500

    # Tabla pivote: Ventas Promedio por Categoría y Tier de Ciudad
    # Reset index para que sea plana
    tier_pref = df.groupby(['Outlet_Location_Type', 'Broad_Category'])['Item_Outlet_Sales'].mean().reset_index()
    
    # Formato para Heatmap (x, y, value)
    heatmap_data = []
    for _, row in tier_pref.iterrows():
        heatmap_data.append({
            "x": row['Outlet_Location_Type'], # Tier 1, 2, 3
            "y": row['Broad_Category'],       # Food, Drinks...
            "value": round(row['Item_Outlet_Sales'], 2)
        })

    return jsonify(heatmap_data)

@app.route('/business-intelligence/bigmart-analisys/dashboards/store-type-comparison')
def get_dashboard_comparison():
    print("Se llamo a get_dashboard_comparison")
    df = get_merged_dashboard_data()
    if df is None: return jsonify({"error": "Data processing error"}), 500

    # Agrupar por Tipo de Tienda y Cluster
    grouped = df.groupby(['Outlet_Type', 'Cluster_Label'])['Item_Outlet_Sales'].sum().reset_index()
    
    # Calcular totales por tipo de tienda para sacar porcentajes
    totals = df.groupby('Outlet_Type')['Item_Outlet_Sales'].sum().to_dict()
    
    response = {}
    for outlet in grouped['Outlet_Type'].unique():
        subset = grouped[grouped['Outlet_Type'] == outlet]
        total_sales = totals[outlet]
        
        breakdown = []
        for _, row in subset.iterrows():
            breakdown.append({
                "cluster": row['Cluster_Label'],
                "absolute_sales": round(row['Item_Outlet_Sales'], 2),
                "percentage": round((row['Item_Outlet_Sales'] / total_sales) * 100, 2)
            })
            
        response[outlet] = {
            "total_sales_scale": round(total_sales, 2), # Para gráfico de Escala
            "mix": breakdown                            # Para gráfico de Mix 100%
        }
        
    return jsonify(response)

@app.route('/business-intelligence/bigmart-analisys/dashboards/treemap-data')
def get_dashboard_treemap_data():
    """
    Estructura optimizada para Plotly Treemap
    Jerarquía: Root → Stores → Clusters → Sales
    """
    print("Se llamo a get_dashboard_treemap_data")
    
    json_path = os.path.join(BASE_DATA_PATH, 'Processed', 'store_hierarchy_final.json')
    
    if not os.path.exists(json_path):
        return jsonify({"error": "Hierarchy JSON not found"}), 404
    
    try:
        with open(json_path, 'r') as f:
            stores = json.load(f)
        
        # Inicializar estructura para Plotly Treemap
        treemap_data = {
            "labels": [],
            "parents": [],
            "values": [],
            "text": [],
            "colors": []  # Para colorear por tipo de tienda
        }
        
        # Color mapping para tipos de tienda
        store_type_colors = {
            "Grocery Store": "#FF6B6B",
            "Supermarket Type1": "#4ECDC4",
            "Supermarket Type2": "#45B7D1",
            "Supermarket Type3": "#96CEB4"
        }
        
        # 1. Root Node
        total_sales = sum(s['total_sales'] for s in stores)
        treemap_data["labels"].append("BigMart Sales")
        treemap_data["parents"].append("")
        treemap_data["values"].append(total_sales)
        treemap_data["text"].append(f"Total: ${total_sales:,.0f}")
        treemap_data["colors"].append("#2C3E50")
        
        # 2. Store Level
        for store in stores:
            store_id = store['id']
            store_label = f"{store_id}<br>{store['type']}"
            
            treemap_data["labels"].append(store_label)
            treemap_data["parents"].append("BigMart Sales")
            treemap_data["values"].append(store['total_sales'])
            treemap_data["text"].append(
                f"{store['type']}<br>"
                f"Location: {store['location']}<br>"
                f"Sales: ${store['total_sales']:,.0f}"
            )
            treemap_data["colors"].append(store_type_colors.get(store['type'], "#95A5A6"))
            
            # 3. Cluster Level (dentro de cada tienda)
            for cluster_info in store['breakdown']:
                cluster_label = f"{cluster_info['cluster']}"
                cluster_full_id = f"{store_id}_{cluster_label}"
                
                treemap_data["labels"].append(cluster_full_id)
                treemap_data["parents"].append(store_label)
                treemap_data["values"].append(cluster_info['value'])
                treemap_data["text"].append(
                    f"{cluster_info['cluster']}<br>"
                    f"{cluster_info['percent']}% of store<br>"
                    f"${cluster_info['value']:,.0f}"
                )
                treemap_data["colors"].append(store_type_colors.get(store['type'], "#95A5A6"))
        
        return jsonify(treemap_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/dashboards/sunburst-data')
def get_dashboard_sunburst_data():
    """
    Estructura para Plotly Sunburst Chart
    Centro: Stores → Anillos: Clusters → Productos Top
    """
    print("Se llamo a get_dashboard_sunburst_data")
    json_path = os.path.join(BASE_DATA_PATH, 'Processed', 'store_hierarchy_final.json')
    
    if not os.path.exists(json_path):
        return jsonify({"error": "Hierarchy JSON not found"}), 404
    
    try:
        with open(json_path, 'r') as f:
            stores = json.load(f)
        
        sunburst_data = {
            "labels": [],
            "parents": [],
            "values": [],
            "text": []
        }
        
        # Root
        sunburst_data["labels"].append("BigMart")
        sunburst_data["parents"].append("")
        sunburst_data["values"].append(sum(s['total_sales'] for s in stores))
        sunburst_data["text"].append(f"Total Sales: ${sunburst_data['values'][0]:,.0f}")
        
        # Stores
        for store in stores:
            store_id = store['id']
            store_name = f"{store_id} ({store['type']})"
            
            sunburst_data["labels"].append(store_name)
            sunburst_data["parents"].append("BigMart")
            sunburst_data["values"].append(store['total_sales'])
            sunburst_data["text"].append(f"{store['location']} - ${store['total_sales']:,.0f}")
            
            # Clusters
            for cluster_info in store['breakdown']:
                cluster_name = cluster_info['cluster']
                cluster_id = f"{store_id}_{cluster_name}"
                
                sunburst_data["labels"].append(cluster_id)
                sunburst_data["parents"].append(store_name)
                sunburst_data["values"].append(cluster_info['value'])
                sunburst_data["text"].append(f"{cluster_info['percent']}%")
                
                # Top 3 Products (opcional, para drill-down)
                for i, product in enumerate(store['top_products'][:3]):
                    if product['Broad_Category'] in cluster_name or 'Non-Edible' in cluster_name:
                        product_id = f"{cluster_id}_{product['Item_Identifier']}"
                        sunburst_data["labels"].append(product['Item_Identifier'])
                        sunburst_data["parents"].append(cluster_id)
                        sunburst_data["values"].append(product['Item_Outlet_Sales'])
                        sunburst_data["text"].append(f"${product['Item_Outlet_Sales']:,.0f}")
        
        return jsonify(sunburst_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/dashboards/bubble-map')
def get_dashboard_bubble_map():
    """
    Datos para Bubble Chart
    X: Año de establecimiento
    Y: Ventas totales
    Tamaño: Ventas totales
    Color: Tipo de tienda
    """
    print("Se llamo a get_dashboard_bubble_map")
    json_path = os.path.join(BASE_DATA_PATH, 'Processed', 'store_hierarchy_final.json')
    
    if not os.path.exists(json_path):
        return jsonify({"error": "Hierarchy JSON not found"}), 404
    
    try:
        with open(json_path, 'r') as f:
            stores = json.load(f)
        
        bubble_data = []
        
        # Mapeo de ubicaciones a valores numéricos para eje secundario
        location_map = {"Tier 1": 3, "Tier 2": 2, "Tier 3": 1}
        
        for store in stores:
            bubble_data.append({
                "id": store['id'],
                "x": store['year_established'],
                "y": store['total_sales'],
                "size": store['total_sales'] / 1000,  # Normalizar para tamaño razonable
                "color": store['type'],
                "location": store['location'],
                "location_numeric": location_map.get(store['location'], 2),
                "size_category": store.get('size', 'Unknown'),
                "dominant_tier": store['dominant_price_tier'],
                "text": (
                    f"<b>{store['id']}</b><br>"
                    f"Type: {store['type']}<br>"
                    f"Location: {store['location']}<br>"
                    f"Size: {store.get('size', 'N/A')}<br>"
                    f"Established: {store['year_established']}<br>"
                    f"Sales: ${store['total_sales']:,.0f}<br>"
                    f"Price Focus: {store['dominant_price_tier']}"
                )
            })
        
        return jsonify({
            "data": bubble_data,
            "metadata": {
                "x_label": "Year Established",
                "y_label": "Total Sales ($)",
                "size_label": "Sales Volume",
                "color_categories": list(set(s['type'] for s in stores))
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/dashboards/store-cards')
def get_dashboard_store_cards():
    """
    Datos para crear tarjetas informativas de cada tienda
    Útil para vista de resumen tipo dashboard ejecutivo
    """
    print("Se llamo a get_dashboard_store_cards")
    json_path = os.path.join(BASE_DATA_PATH, 'Processed', 'store_hierarchy_final.json')
    
    if not os.path.exists(json_path):
        return jsonify({"error": "Hierarchy JSON not found"}), 404
    
    try:
        with open(json_path, 'r') as f:
            stores = json.load(f)
        
        cards_data = []
        
        for store in stores:
            # Identificar cluster dominante
            dominant_cluster = max(store['breakdown'], key=lambda x: x['value'])
            
            # Top 3 productos
            top_3_sales = sum(p['Item_Outlet_Sales'] for p in store['top_products'][:3])
            
            cards_data.append({
                "store_id": store['id'],
                "store_type": store['type'],
                "location": store['location'],
                "size": store.get('size', 'Not Specified'),
                "year_established": store['year_established'],
                "years_in_operation": 2013 - store['year_established'],
                "total_sales": round(store['total_sales'], 2),
                "dominant_cluster": {
                    "name": dominant_cluster['cluster'],
                    "percentage": dominant_cluster['percent'],
                    "value": round(dominant_cluster['value'], 2)
                },
                "price_focus": store['dominant_price_tier'],
                "top_products_contribution": round((top_3_sales / store['total_sales']) * 100, 2),
                "cluster_diversity": len(store['breakdown']),
                "performance_tier": (
                    "High" if store['total_sales'] > 2000000 else
                    "Medium" if store['total_sales'] > 1000000 else
                    "Low"
                )
            })
        
        # Ordenar por ventas totales (descendente)
        cards_data_sorted = sorted(cards_data, key=lambda x: x['total_sales'], reverse=True)
        
        return jsonify({
            "stores": cards_data_sorted,
            "summary": {
                "total_stores": len(cards_data_sorted),
                "total_sales": sum(s['total_sales'] for s in cards_data_sorted),
                "avg_sales_per_store": round(sum(s['total_sales'] for s in cards_data_sorted) / len(cards_data_sorted), 2),
                "store_type_distribution": {
                    store_type: len([s for s in cards_data_sorted if s['store_type'] == store_type])
                    for store_type in set(s['store_type'] for s in cards_data_sorted)
                }
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys')
def overview_bigmart():
    html_path = os.path.join('9th_quarter','Business_Intelligence','HW4','index.html')
    return render_template(html_path)

@app.route('/business-intelligence/bigmart-analisys/eda')
def eda_bigmart():
    html_path = os.path.join('9th_quarter','Business_Intelligence','HW4','Scripts','eda.html')
    return render_template(html_path)

@app.route('/business-intelligence/bigmart-analisys/modeling')
def modeling_bigmart():
    html_path = os.path.join('9th_quarter','Business_Intelligence','HW4','Scripts','modeling.html')
    return render_template(html_path)

@app.route('/business-intelligence/bigmart-analisys/dashboards')
def dashboard_bigmart():
    html_path = os.path.join('9th_quarter','Business_Intelligence','HW4','Scripts','dashboards.html')
    return render_template(html_path)

# # === Credit Risk
# # Cargar modelo de ML (al inicio de la app)
# MODEL_PATH        = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'PR3', 'Docs', 'models', 'credit_risk_model.pkl')
# CONFIG_PATH       = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'PR3', 'Docs', 'models', 'web_config.json')
# FEATURE_DICT_PATH = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'PR3', 'Docs', 'models', 'feature_dictionary.csv')

# # Cargar modelo
# try:
#     with open(MODEL_PATH, 'rb') as f: credit_model = pickle.load(f)
#     with open(CONFIG_PATH, 'r') as f: model_config = json.load(f)
#     feature_dict = pd.read_csv(FEATURE_DICT_PATH)
#     print("Modelo de crédito cargado exitosamente")
# except Exception as e:
#     print(f"Error al cargar el modelo: {e}")
#     credit_model = None

# @app.route('/business-intelligence/credit-risk')
# def credit_risk():
#     html_path = os.path.join('9th_quarter','Business_Intelligence','PR3','index.html')
#     return render_template(html_path)

# @app.route('/business-intelligence/credit-risk/predict', methods=['POST'])
# def predict_credit_risk():
#     print('Recibio una consulta para prediccion...')
#     try:
#         # Verificar si el modelo está cargado
#         if credit_model is None:
#             return jsonify({
#                 'error': 'Modelo no disponible',
#                 'message': 'El modelo de riesgo crediticio no está cargado correctamente'
#             }), 500

#         # Obtener datos del request
#         data = request.get_json()
        
#         if not data:
#             return jsonify({
#                 'error': 'Datos no proporcionados',
#                 'message': 'Se esperaba un JSON con los datos del cliente'
#             }), 400

#         # Crear DataFrame con los datos de entrada
#         input_data = {}
        
#         # Extraer nombres de características del modelo_config
#         feature_names = [feature['name'] for feature in model_config['features']]
        
#         # Mapear los datos del formulario a las características esperadas por el modelo
#         feature_mapping = {
#             # Variables numéricas básicas
#             'month_credit_duration': float(data.get('month_credit_duration', 0)),
#             'credit_amount': float(data.get('credit_amount', 0)),
#             'pct_fee_income': float(data.get('pct_fee_income', 0)),
#             'age': float(data.get('age', 0)),
#             'num_existing_credits': float(data.get('num_existing_credits', 0)),
            
#             # Variables transformadas (se calculan si no vienen)
#             'credit_to_duration_ratio': float(data.get('credit_to_duration_ratio', 
#                 float(data.get('credit_amount', 0)) / max(float(data.get('month_credit_duration', 1)), 1))),
#             'age_squared': float(data.get('age_squared', 
#                 float(data.get('age', 0)) ** 2)),
#             'log_credit_amount': float(data.get('log_credit_amount', 
#                 np.log1p(max(float(data.get('credit_amount', 0)), 0)))),
            
#             # Variables binarias creadas
#             'high_duration': int(float(data.get('month_credit_duration', 0)) > 24),
#             'high_amount': int(float(data.get('credit_amount', 0)) > 3972),
#             'high_risk_profile': int(data.get('high_risk_profile', 0)),
#         }

#         # Agregar variables one-hot encoded (categóricas)
#         categorical_vars = [
#             'status_sex', 'debtors', 'property', 'housing', 'other_installments',
#             'telephone', 'foreign_worker', 'status_checking_account', 
#             'credit_history', 'purpose', 'savings_type', 'years_of_employment', 'job'
#         ]

#         for var in categorical_vars:
#             value = data.get(var, '')
#             # Para cada posible categoría de la variable
#             all_categories = [col for col in feature_names if col.startswith(f"{var}_")]
#             for category in all_categories:
#                 category_value = category.replace(f"{var}_", "")
#                 input_data[category] = 1 if value == category_value else 0

#         # Combinar todos los datos
#         input_data.update(feature_mapping)

#         # Crear DataFrame asegurando el orden correcto de características
#         expected_features = feature_names
#         input_df = pd.DataFrame([input_data])
        
#         # Asegurar que tenemos todas las características esperadas
#         for feature in expected_features:
#             if feature not in input_df.columns:
#                 input_df[feature] = 0  # Valor por defecto para características faltantes

#         # Reordenar columnas al orden esperado por el modelo
#         input_df = input_df[expected_features]

#         # Realizar predicción
#         probability = credit_model.predict_proba(input_df)[0]
#         risk_probability = probability[0]  # Probabilidad de ser mal pagador (clase 0)
#         good_probability = probability[1]  # Probabilidad de ser buen pagador (clase 1)

#         # Aplicar umbral óptimo
#         threshold = model_config['threshold']
#         prediction = 0 if risk_probability >= threshold else 1  # 0 = malo, 1 = bueno

#         # Interpretación de resultados
#         risk_level = "Alto Riesgo" if prediction == 0 else "Bajo Riesgo"
#         recommendation = "No aprobar crédito" if prediction == 0 else "Aprobar crédito"
        
#         # Calcular score de confianza
#         confidence_score = risk_probability if prediction == 0 else good_probability

#         # Preparar respuesta
#         response = {
#             'prediction': prediction,
#             'risk_level': risk_level,
#             'recommendation': recommendation,
#             'probabilities': {
#                 'bad_payer_probability': round(float(risk_probability), 4),
#                 'good_payer_probability': round(float(good_probability), 4)
#             },
#             'confidence_score': round(float(confidence_score), 4),
#             'threshold_used': float(threshold),
#             'features_used': len(expected_features)
#         }
#         return jsonify(response)

#     except Exception as e:
#         print(f"Error en predicción: {str(e)}")
#         print(f"Traceback: {traceback.format_exc()}")
#         return jsonify({
#             'error': 'Error en la predicción',
#             'message': str(e)
#         }), 500



# # ===== Visualization Tools II
# # === Kafka
# kafka_modules_path = os.path.join(location_path, 'Files', '9th_quarter', 'Visualization_Tools_II', 'Kafka_Clicker')
# sys.path.append(kafka_modules_path)

# try:
#     from producer import click_producer #type:ignore
#     from consumer import click_consumer #type:ignore
#     print("Módulos de Kafka importados correctamente.")
# except ImportError as e:
#     print(f"Error importando módulos de Kafka: {e}")
#     # Definimos mocks por si falla la importación para que no crashee la app entera
#     click_producer = None
#     click_consumer = None

# @app.route('/visualization-tools-ii/kafka-clicker')
# def kafka_clicker_gem():
#     html_path = os.path.join('9th_quarter','Visualization_Tools_II','Kafka_Clicker','clicker.html')
#     return render_template(html_path)

# @app.route('/visualization-tools-ii/kafka-dashboard')
# def kafka_dashboard_gem():
#     html_path = os.path.join('9th_quarter','Visualization_Tools_II','Kafka_Clicker','dashboard.html')
#     return render_template(html_path)

# @app.route('/visualization-tools-ii/kafka/click', methods=['POST'])
# def send_click():
#     print('Click...')
#     if not click_producer:
#         return jsonify({'status': 'error', 'message': 'Producer not loaded'}), 500

#     data = request.json
#     click_type = data.get('type') # Espera 'cheers' o 'fuck'
    
#     if click_type not in ['cheers', 'fuck']:
#         return jsonify({'status': 'error', 'message': 'Invalid click type'}), 400

#     # Usar el producer importado para enviar a Kafka
#     success = click_producer.send_click(click_type)
    
#     if success:
#         return jsonify({'status': 'success', 'message': f'Click {click_type} sent!'})
#     else:
#         return jsonify({'status': 'error', 'message': 'Failed to send to Kafka'}), 500

# @app.route('/visualization-tools-ii/kafka/data', methods=['GET'])
# def get_kafka_data():
#     print('Dashboards...')
#     if not click_consumer:
#         return jsonify({'status': 'error', 'message': 'Consumer not loaded'}), 500
    
#     # Obtener datos procesados del consumer (Totales y Recientes)
#     data = click_consumer.get_data()
#     return jsonify(data)





# # ===== General
# @app.route('/pdf/engineering-week')
# def serve_engineering_week_pdf():
#     pdf_file_path = os.path.join(location_path, 'Files', '8th_quarter', 'Engineering_Week_Report.pdf')
    
#     if os.path.exists(pdf_file_path):
#         return send_file(pdf_file_path, as_attachment=False, mimetype='application/pdf')
#     else:
#         abort(404)




# # ===== Digital Economy
# @app.route('/digital-economy/smart-factory-data-pipeline-challenge')
# def smart_factory_data_pipeline_challenge():
#     html_path = os.path.join('9th_quarter','Digital_Economy','Smart_Irrigation_Pipeline.html')
#     return render_template(html_path)

# @app.route('/digital-economy/business-model')
# def amazon_case_business():
#     html_path = os.path.join('9th_quarter','Digital_Economy','Amazon_case_business.html')
#     return render_template(html_path)




# # ===== Social Network Analysis
# @app.route('/social-network-analysis/friendship-paradox')
# def friendship_paradox():
#     html_path = os.path.join('8th_quarter','Network_Analysis','HW5','friendship_paradox_infographic.html')
#     return render_template(html_path)




# # ===== Visualization Tools I
# @app.route('/visualization-tools-i/badges-diego-monroy')
# def badges():
#     html_path = os.path.join('8th_quarter','Visualization_Tools','Badges','badges.html')
#     certs = [
#         {
#             "title"    : "Activity 04 - Get Started With Looker",
#             "filename" : "Get Started With Looker.png",
#             "type"     : "image",
#         },
#         {
#             "title"    : "Activity 05 - BI and Analytics with Looker Learning Path",
#             "filename" : "BI and Analytics.png",
#             "type"     : "image",
#         },
#         {
#             "title"    : "Activity 09 - Get started with Microsoft data analytics",
#             "filename" : "Get started with Microsoft data analytics.pdf",
#             "type"     : "pdf",
#         },
#         {
#             "title"    : "Activity A09 - Model data with Power BI",
#             "filename" : "Model data with Power BI.pdf",
#             "type"     : "pdf",
#         },
#         {
#             "title"    : "Activity A10 - Build Power BI visuals and reports",
#             "filename" : "Build Power BI visuals and reports.pdf",
#             "type"     : "pdf",
#         },
#     ]
#     return render_template(html_path, certs=certs)

# @app.route('/visualization-tools-i/wikistream-analytics')
# def wikistream_analytics():
#     html_path = os.path.join('8th_quarter','Visualization_Tools','WikiStream','stream.html')
#     return render_template(html_path)

# @app.route('/visualization-tools-i/engineering-week')
# def eng_week_visualization():
#     html_path = os.path.join('8th_quarter','Visualization_Tools','Engineering_week','report.html')
#     pdf_path = '/pdf/engineering-week'
#     return render_template(html_path,pdf_path=pdf_path)




# # ===== English VIII
# @app.route('/english-viii/ted-talk')
# def ted_talk():
#     html_path = os.path.join('8th_quarter','English','TED_Talk','talk.html')
#     return render_template(html_path)
