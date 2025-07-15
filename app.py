import os
from flask import Flask, render_template

location_path = os.path.dirname(__file__)
app = Flask(
    __name__,
    template_folder = os.path.join(location_path,'Files'),
    static_folder   = os.path.join(location_path,'Files')
)

# ===== General
@app.route('/')
def index():
    
    materias = {
        'Visualization Tools':[
            'Badges - Diego Monroy',
            'WikiStream Analytics',
        ],
        'Social Network Analysis':[
            'Friendship Paradox'
        ]
    }

    return render_template('/index.html', materias = materias)


# ===== Social Network Analysis
@app.route('/social-network-analysis/friendship-paradox')
def friendship_paradox():
    html_path = os.path.join('8th_quarter','Network_Analysis','HW5','friendship_paradox_infographic.html')
    return render_template(html_path)


# ===== Visualization Tools
@app.route('/visualization-tools/badges-diego-monroy')
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

@app.route('/visualization-tools/wikistream-analytics')
def wikistream_analytics():
    html_path = os.path.join('8th_quarter','Visualization_Tools','WikiStream','stream.html')
    return render_template(html_path)