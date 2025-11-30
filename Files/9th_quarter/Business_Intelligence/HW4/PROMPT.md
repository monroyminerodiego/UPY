### Aditional info
``` bash
[diego@DiegoMonroy]~/PROGRAMACION/VPS/UPY% ls
app.py  docker-compose.yml  Dockerfile  Files  mongo-init.js  README.md  requirements.txt
[diego@DiegoMonroy]~/PROGRAMACION/VPS/UPY% tree Files/9th_quarter/Business_Intelligence/HW4 
Files/9th_quarter/Business_Intelligence/HW4
├── Data
│   ├── Processed
│   │   ├── product_level_interpretation.csv
│   │   ├── product_level_modeling.csv
│   │   ├── product_level_with_clusters.csv
│   │   └── store_hierarchy_final.json
│   └── Raw
│       └── train.csv
├── Docs
│   ├── Context.pdf
│   ├── EDA.md
│   └── Instructions.pdf
├── index.html
├── Notebooks
│   ├── fase_a.ipynb
│   ├── fase_b.ipynb
│   ├── fase_c.ipynb
│   └── fase_d.ipynb
├── PROMPT.md
├── README.md
└── Scripts
    └── stringify.py

7 directories, 16 files
```

``` app.py
import os, pickle, json, traceback, sys
import numpy as np, pandas as pd
from flask import Flask, render_template, send_file, abort, request, jsonify

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
@app.route('/business-intelligence/bigmart-analisys/eda-summary')
def bigmart_eda_summary():
    """Sirve resumen del EDA para la Vista 1"""
    print('Se llamo a bigmart_eda_summary')
    try:
        # Cargar datos raw
        df = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Raw/train.csv'))
        
        # Estadísticas generales
        summary = {
            'total_records': int(df.shape[0]),
            'total_features': int(df.shape[1]),
            'unique_products': int(df['Item_Identifier'].nunique()),
            'unique_stores': int(df['Outlet_Identifier'].nunique()),
            
            # Valores faltantes
            'missing_values': {
                'Item_Weight': {
                    'count': int(df['Item_Weight'].isnull().sum()),
                    'percentage': float(df['Item_Weight'].isnull().sum() / len(df) * 100)
                },
                'Outlet_Size': {
                    'count': int(df['Outlet_Size'].isnull().sum()),
                    'percentage': float(df['Outlet_Size'].isnull().sum() / len(df) * 100)
                }
            },
            
            # Estadísticas de ventas
            'sales_stats': {
                'mean': float(df['Item_Outlet_Sales'].mean()),
                'median': float(df['Item_Outlet_Sales'].median()),
                'min': float(df['Item_Outlet_Sales'].min()),
                'max': float(df['Item_Outlet_Sales'].max()),
                'skewness': float(df['Item_Outlet_Sales'].skew())
            },
            
            # Distribución de categorías
            'fat_content_dist': df['Item_Fat_Content'].value_counts().to_dict(),
            'outlet_type_dist': df['Outlet_Type'].value_counts().to_dict(),
            'item_type_dist': df['Item_Type'].value_counts().head(10).to_dict()
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/distributions')
def bigmart_distributions():
    """Sirve datos de distribuciones para histogramas"""
    print("Se llamo a bigmart_distributions")
    try:
        df = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Raw/train.csv'))
        
        distributions = {
            'sales': df['Item_Outlet_Sales'].tolist(),
            'mrp': df['Item_MRP'].tolist(),
            'visibility': df['Item_Visibility'].tolist(),
            'weight': df['Item_Weight'].dropna().tolist()
        }
        
        return jsonify(distributions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/outliers')
def bigmart_outliers():
    """Calcula outliers usando IQR para cada variable numérica"""
    print("Se llamo a bigmart_outliers")
    try:
        df = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Raw/train.csv'))
        numeric_cols = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Item_Outlet_Sales']
        
        outliers_info = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            outliers_info[col] = {
                'count': int(len(outliers)),
                'percentage': float(len(outliers) / len(df) * 100),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }
        
        return jsonify(outliers_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/clustering-metrics')
def bigmart_clustering_metrics():
    """Sirve métricas de clustering (silhouette e inercia)"""
    print("Se llamo a bigmart_clustering_metrics")
    try:
        # Estos datos vienen de tu fase_c.ipynb
        # Los valores que mostraste en los prints
        metrics = {
            'k_range': list(range(2, 31)),
            'silhouette_scores': [
                0.3156, 0.2776, 0.3109, 0.2927, 0.2927,  # K=2 a K=6
                # Agrega valores interpolados o reales para K=7-30
                0.2800, 0.2700, 0.2600, 0.2500, 0.2144,  # K=7-10
                0.2200, 0.2180, 0.2160, 0.2140, 0.2116,  # K=11-15
                0.2100, 0.2080, 0.2060, 0.2040, 0.2020,  # K=16-20
                0.2000, 0.1980, 0.1960, 0.1940, 0.1920,  # K=21-25
                0.1900, 0.1880, 0.1860, 0.1840, 0.1820   # K=26-30
            ],
            'inertia_values': [
                14103.2, 11347.1, 9413.4, 8044.4, 7234.0,  # K=2 a K=6
                6800, 6400, 6200, 6000, 5923.2,  # K=7-10
                5600, 5400, 5300, 5200, 4940.5,  # K=11-15
                4800, 4700, 4600, 4500, 4400,    # K=16-20
                4300, 4200, 4100, 4000, 3900,    # K=21-25
                3800, 3700, 3600, 3500, 3400     # K=26-30
            ],
            'optimal_k': 4,
            'optimal_k_silhouette': 0.3109
        }
        
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/pca-visualization')
def bigmart_pca():
    """Sirve datos de PCA para visualización de clusters"""
    print("Se llamo a bigmart_pca")
    try:
        # Cargar el archivo con clusters ya asignados
        df_clusters = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Processed/product_level_with_clusters.csv'))
        
        # Para simplificar, usaremos Total_Sales y Avg_MRP como "pseudo-PCA"
        # En producción, deberías calcular PCA real
        pca_data = []
        for _, row in df_clusters.head(200).iterrows():  # Limitar para rendimiento
            pca_data.append({
                'pc1': float(row['Total_Sales'] / 1000),  # Normalizar
                'pc2': float(row['Avg_MRP'] / 10),
                'cluster': int(row['Cluster']),
                'item_id': row['Item_Identifier']
            })
        
        return jsonify(pca_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/cluster-profiles')
def bigmart_cluster_profiles():
    """Sirve perfiles de cada cluster"""
    print("Se llamo a bigmart_cluster_profiles")
    try:
        df = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Processed/product_level_with_clusters.csv'))
        
        profiles = []
        for cluster_id in sorted(df['Cluster'].unique()):
            cluster_data = df[df['Cluster'] == cluster_id]
            
            profiles.append({
                'cluster_id': int(cluster_id),
                'cluster_label': cluster_data['Cluster_Label'].mode()[0],
                'count': int(len(cluster_data)),
                'avg_sales': float(cluster_data['Total_Sales'].mean()),
                'avg_mrp': float(cluster_data['Avg_MRP'].mean()),
                'avg_store_count': float(cluster_data['Store_Count'].mean()),
                'dominant_category': cluster_data['Broad_Category'].mode()[0]
            })
        
        return jsonify(profiles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/store-hierarchy')
def bigmart_store_hierarchy():
    """Sirve el JSON de jerarquía de tiendas ya procesado"""
    print("Se llamo a bigmart_store_hierarchy")
    try:
        json_path = os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Processed/store_hierarchy_final.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys/store-mix-analysis')
def bigmart_store_mix():
    """Análisis de mezcla de clusters por tienda"""
    print("Se llamo a bigmart_store_mix")
    try:
        # Cargar datos raw y clusters
        df_raw = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Raw/train.csv'))
        df_clusters = pd.read_csv(os.path.join(location_path, 'Files/9th_quarter/Business_Intelligence/HW4/Data/Processed/product_level_with_clusters.csv'))
        
        # Merge
        df_merged = df_raw.merge(df_clusters[['Item_Identifier', 'Cluster', 'Cluster_Label']], on='Item_Identifier', how='left')
        
        # Agrupar por tienda y cluster
        store_mix = []
        for store_id in df_merged['Outlet_Identifier'].unique():
            store_data = df_merged[df_merged['Outlet_Identifier'] == store_id]
            
            mix_breakdown = []
            for cluster_id in store_data['Cluster'].unique():
                cluster_sales = store_data[store_data['Cluster'] == cluster_id]['Item_Outlet_Sales'].sum()
                mix_breakdown.append({
                    'cluster_id': int(cluster_id),
                    'cluster_label': store_data[store_data['Cluster'] == cluster_id]['Cluster_Label'].mode()[0],
                    'sales': float(cluster_sales),
                    'percentage': float(cluster_sales / store_data['Item_Outlet_Sales'].sum() * 100)
                })
            
            store_mix.append({
                'store_id': store_id,
                'store_type': store_data['Outlet_Type'].iloc[0],
                'total_sales': float(store_data['Item_Outlet_Sales'].sum()),
                'mix': mix_breakdown
            })
        
        return jsonify(store_mix)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence/bigmart-analisys')
def clustering_bi():
    html_path = os.path.join('9th_quarter','Business_Intelligence','HW4','index.html')
    return render_template(html_path)
```

### Prompt
Te estoy compartiendo todo el contexto de mi proyecto, desde como hice las notebooks de cada fase, como esta organizado cada carpeta, el overview de la data raw.
En esta iteración ya estoy en la Fase E, la de construir los dashboards de business intelligence. Quiero que el dashboard sea hecho con d3.js y que viva en el index.html
Quiero que me ayudes a hacer la vista web, que contenga 3 principales vistas: 1. EDA / Cleaning, 2. Decision de modelaje, 3. Analisis de información
En la vista 1 quiero que abarques lo de la fase a y b, que incluye el EDA (Quiero que me des una descripcion general de la data, el analisis de las distribuciones, analisis de regitros faltantes, outliers) y el manejo de esas situaciones, como la limpieza de datos granular, el feature engineering, la forma de manejar outliers y faltantes.
En la vista 2 quiero que abarques lo de la dase c, que incluye las metricas solhouette e inercia, el analisis de la decision, el entrenamiento y la ilusion visual del PCA.
En la vista 3 quiero que abarques lo de la fase d, que es donde ya tenemos como tal los dashboards de business intelligence. Quiero que en esta vista incluyas las graficas para poder hacer la visuaizacion de la información, además de que quiero que me des una breve explicacion de la grafica. Toma en cuenta que las instrucciones piden vista de cluster de productos y mezcla de clusters por tienda, por lo que quiero que esas dos secciones se incluyan dentro de la vista 3. Quiero que agregues a Diego Monroy | Ariel Buenfil | Alan Valbuena | Damaris Dzul | Sergio Barrera | Moises Carrillo como autores y que tenga un boton de home que me mande a la ruta '/'.
Tomando en cuenta toda la estructura de mi proyecto, ayudame a generar el archivo index.html, pero asegurate de solo usar html, css, y js (Puedes usar herramientas como tailwind, d3.js, etc., pero que no sea fuera de los limites utilizables para flask)