import flask as fl
from werkzeug.utils import secure_filename
import os

app = fl.Flask(__name__)
uploaded_file_path = ''

app.config["UPLOAD_FOLDER"] = 'static/Downloads'

ALLOWED_EXTENSIONS = set(['csv'])

@app.route("/")
def root():
    return fl.render_template("index.html")

@app.route("/uploaded",methods=['POST'])
def upload():
    global uploaded_file_path
    file = fl.request.files['UploadFile']
    filename = secure_filename(file.filename) #type:ignore
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    return fl.render_template("cleaning.html")

@app.route("/cleaned")
def mmds():
    from static.PY.cleaning_class import Cleaning
    data_cleaned = Cleaning(
        raw_file_path=uploaded_file_path,
        correlation_in_columns=0.49
    )
    return fl.render_template("testing.html")

if __name__ == '__main__':
    app.run(debug=True)