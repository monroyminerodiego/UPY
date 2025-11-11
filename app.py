import os
from flask import Flask, render_template, send_file, abort

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
            "Personalized Web"
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




# ===== Business Intelligence
@app.route('/business-intelligence/credit-risk')
def credit_risk():
    html_path = os.path.join('9th_quarter','Business_Intelligence','PR3','index.html')
    return render_template(html_path)




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
