import os, pickle, json, traceback, sys
import numpy as np, pandas as pd
from flask import Flask, render_template, send_file, abort, request, jsonify

location_path = os.path.dirname(__file__)
app = Flask(
    __name__,
    template_folder = os.path.join(location_path,'Files'),
    static_folder   = os.path.join(location_path,'Files')
)

# ===== Cargar modelo de ML (al inicio de la app)
MODEL_PATH        = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'PR3', 'Docs', 'models', 'credit_risk_model.pkl')
CONFIG_PATH       = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'PR3', 'Docs', 'models', 'web_config.json')
FEATURE_DICT_PATH = os.path.join(location_path, 'Files', '9th_quarter', 'Business_Intelligence', 'PR3', 'Docs', 'models', 'feature_dictionary.csv')

# Cargar modelo
try:
    with open(MODEL_PATH, 'rb') as f: credit_model = pickle.load(f)
    with open(CONFIG_PATH, 'r') as f: model_config = json.load(f)
    feature_dict = pd.read_csv(FEATURE_DICT_PATH)
    print("Modelo de crédito cargado exitosamente")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    credit_model = None
# =====

kafka_modules_path = os.path.join(location_path, 'Files', '9th_quarter', 'Visualization_Tools_II', 'Kafka_Clicker')
sys.path.append(kafka_modules_path)

# Ahora sí podemos importar las instancias globales
try:
    from producer import click_producer #type:ignore
    from consumer import click_consumer #type:ignore
    print("Módulos de Kafka importados correctamente.")
except ImportError as e:
    print(f"Error importando módulos de Kafka: {e}")
    # Definimos mocks por si falla la importación para que no crashee la app entera
    click_producer = None
    click_consumer = None

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
            "Credit Risk"
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




# ===== Visualization Tools II
@app.route('/visualization-tools-ii/kafka-clicker')
def kafka_clicker_gem():
    html_path = os.path.join('9th_quarter','Visualization_Tools_II','Kafka_Clicker','clicker.html')
    return render_template(html_path)

@app.route('/visualization-tools-ii/kafka-dashboard')
def kafka_dashboard_gem():
    html_path = os.path.join('9th_quarter','Visualization_Tools_II','Kafka_Clicker','dashboard.html')
    return render_template(html_path)

@app.route('/visualization-tools-ii/kafka/click', methods=['POST'])
def send_click():
    print('Click...')
    if not click_producer:
        return jsonify({'status': 'error', 'message': 'Producer not loaded'}), 500

    data = request.json
    click_type = data.get('type') # Espera 'cheers' o 'fuck'
    
    if click_type not in ['cheers', 'fuck']:
        return jsonify({'status': 'error', 'message': 'Invalid click type'}), 400

    # Usar el producer importado para enviar a Kafka
    success = click_producer.send_click(click_type)
    
    if success:
        return jsonify({'status': 'success', 'message': f'Click {click_type} sent!'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to send to Kafka'}), 500

@app.route('/visualization-tools-ii/kafka/data', methods=['GET'])
def get_kafka_data():
    print('Dashboards...')
    if not click_consumer:
        return jsonify({'status': 'error', 'message': 'Consumer not loaded'}), 500
    
    # Obtener datos procesados del consumer (Totales y Recientes)
    data = click_consumer.get_data()
    return jsonify(data)





# ===== Business Intelligence
@app.route('/business-intelligence/credit-risk')
def credit_risk():
    html_path = os.path.join('9th_quarter','Business_Intelligence','PR3','index.html')
    return render_template(html_path)

@app.route('/business-intelligence/credit-risk/predict', methods=['POST'])
def predict_credit_risk():
    print('Recibio una consulta para prediccion...')
    try:
        # Verificar si el modelo está cargado
        if credit_model is None:
            return jsonify({
                'error': 'Modelo no disponible',
                'message': 'El modelo de riesgo crediticio no está cargado correctamente'
            }), 500

        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Datos no proporcionados',
                'message': 'Se esperaba un JSON con los datos del cliente'
            }), 400

        # Crear DataFrame con los datos de entrada
        input_data = {}
        
        # Extraer nombres de características del modelo_config
        feature_names = [feature['name'] for feature in model_config['features']]
        
        # Mapear los datos del formulario a las características esperadas por el modelo
        feature_mapping = {
            # Variables numéricas básicas
            'month_credit_duration': float(data.get('month_credit_duration', 0)),
            'credit_amount': float(data.get('credit_amount', 0)),
            'pct_fee_income': float(data.get('pct_fee_income', 0)),
            'age': float(data.get('age', 0)),
            'num_existing_credits': float(data.get('num_existing_credits', 0)),
            
            # Variables transformadas (se calculan si no vienen)
            'credit_to_duration_ratio': float(data.get('credit_to_duration_ratio', 
                float(data.get('credit_amount', 0)) / max(float(data.get('month_credit_duration', 1)), 1))),
            'age_squared': float(data.get('age_squared', 
                float(data.get('age', 0)) ** 2)),
            'log_credit_amount': float(data.get('log_credit_amount', 
                np.log1p(max(float(data.get('credit_amount', 0)), 0)))),
            
            # Variables binarias creadas
            'high_duration': int(float(data.get('month_credit_duration', 0)) > 24),
            'high_amount': int(float(data.get('credit_amount', 0)) > 3972),
            'high_risk_profile': int(data.get('high_risk_profile', 0)),
        }

        # Agregar variables one-hot encoded (categóricas)
        categorical_vars = [
            'status_sex', 'debtors', 'property', 'housing', 'other_installments',
            'telephone', 'foreign_worker', 'status_checking_account', 
            'credit_history', 'purpose', 'savings_type', 'years_of_employment', 'job'
        ]

        for var in categorical_vars:
            value = data.get(var, '')
            # Para cada posible categoría de la variable
            all_categories = [col for col in feature_names if col.startswith(f"{var}_")]
            for category in all_categories:
                category_value = category.replace(f"{var}_", "")
                input_data[category] = 1 if value == category_value else 0

        # Combinar todos los datos
        input_data.update(feature_mapping)

        # Crear DataFrame asegurando el orden correcto de características
        expected_features = feature_names
        input_df = pd.DataFrame([input_data])
        
        # Asegurar que tenemos todas las características esperadas
        for feature in expected_features:
            if feature not in input_df.columns:
                input_df[feature] = 0  # Valor por defecto para características faltantes

        # Reordenar columnas al orden esperado por el modelo
        input_df = input_df[expected_features]

        # Realizar predicción
        probability = credit_model.predict_proba(input_df)[0]
        risk_probability = probability[0]  # Probabilidad de ser mal pagador (clase 0)
        good_probability = probability[1]  # Probabilidad de ser buen pagador (clase 1)

        # Aplicar umbral óptimo
        threshold = model_config['threshold']
        prediction = 0 if risk_probability >= threshold else 1  # 0 = malo, 1 = bueno

        # Interpretación de resultados
        risk_level = "Alto Riesgo" if prediction == 0 else "Bajo Riesgo"
        recommendation = "No aprobar crédito" if prediction == 0 else "Aprobar crédito"
        
        # Calcular score de confianza
        confidence_score = risk_probability if prediction == 0 else good_probability

        # Preparar respuesta
        response = {
            'prediction': prediction,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'probabilities': {
                'bad_payer_probability': round(float(risk_probability), 4),
                'good_payer_probability': round(float(good_probability), 4)
            },
            'confidence_score': round(float(confidence_score), 4),
            'threshold_used': float(threshold),
            'features_used': len(expected_features)
        }
        return jsonify(response)

    except Exception as e:
        print(f"Error en predicción: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Error en la predicción',
            'message': str(e)
        }), 500



# ===== General
@app.route('/pdf/engineering-week')
def serve_engineering_week_pdf():
    pdf_file_path = os.path.join(location_path, 'Files', '8th_quarter', 'Engineering_Week_Report.pdf')
    
    if os.path.exists(pdf_file_path):
        return send_file(pdf_file_path, as_attachment=False, mimetype='application/pdf')
    else:
        abort(404)




# ===== Digital Economy
@app.route('/digital-economy/smart-factory-data-pipeline-challenge')
def smart_factory_data_pipeline_challenge():
    html_path = os.path.join('9th_quarter','Digital_Economy','Smart_Irrigation_Pipeline.html')
    return render_template(html_path)

@app.route('/digital-economy/business-model')
def amazon_case_business():
    html_path = os.path.join('9th_quarter','Digital_Economy','Amazon_case_business.html')
    return render_template(html_path)




# ===== Social Network Analysis
@app.route('/social-network-analysis/friendship-paradox')
def friendship_paradox():
    html_path = os.path.join('8th_quarter','Network_Analysis','HW5','friendship_paradox_infographic.html')
    return render_template(html_path)




# ===== Visualization Tools I
@app.route('/visualization-tools-i/badges-diego-monroy')
def badges():
    html_path = os.path.join('8th_quarter','Visualization_Tools','Badges','badges.html')
    certs = [
        {
            "title"    : "Activity 04 - Get Started With Looker",
            "filename" : "Get Started With Looker.png",
            "type"     : "image",
        },
        {
            "title"    : "Activity 05 - BI and Analytics with Looker Learning Path",
            "filename" : "BI and Analytics.png",
            "type"     : "image",
        },
        {
            "title"    : "Activity 09 - Get started with Microsoft data analytics",
            "filename" : "Get started with Microsoft data analytics.pdf",
            "type"     : "pdf",
        },
        {
            "title"    : "Activity A09 - Model data with Power BI",
            "filename" : "Model data with Power BI.pdf",
            "type"     : "pdf",
        },
        {
            "title"    : "Activity A10 - Build Power BI visuals and reports",
            "filename" : "Build Power BI visuals and reports.pdf",
            "type"     : "pdf",
        },
    ]
    return render_template(html_path, certs=certs)

@app.route('/visualization-tools-i/wikistream-analytics')
def wikistream_analytics():
    html_path = os.path.join('8th_quarter','Visualization_Tools','WikiStream','stream.html')
    return render_template(html_path)

@app.route('/visualization-tools-i/engineering-week')
def eng_week_visualization():
    html_path = os.path.join('8th_quarter','Visualization_Tools','Engineering_week','report.html')
    pdf_path = '/pdf/engineering-week'
    return render_template(html_path,pdf_path=pdf_path)




# ===== English VIII
@app.route('/english-viii/ted-talk')
def ted_talk():
    html_path = os.path.join('8th_quarter','English','TED_Talk','talk.html')
    return render_template(html_path)
