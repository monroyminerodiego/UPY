from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    
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
            "filename" : "Get started with Microsoft data analytics.png",
            "type"     : "image",
        },
    ]
    return render_template('index.html', certs=certs)
