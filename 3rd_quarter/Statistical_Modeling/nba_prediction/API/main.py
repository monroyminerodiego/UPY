import flask as fl
from werkzeug.utils import secure_filename
import os

app = fl.Flask(__name__,template_folder='static/HTML/')
uploaded_file_path = ''
app.config["UPLOAD_FOLDER"] = 'static/Downloads'

ALLOWED_EXTENSIONS = set(['csv'])

@app.route("/")
def root():
    return fl.render_template('views/index.html')

@app.route("/uploaded",methods=['POST'])
def upload():
    global uploaded_file_path
    file = fl.request.files['UploadFile']
    filename = secure_filename(file.filename) #type:ignore
    uploaded_file_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(uploaded_file_path)
    return fl.render_template("views/cleaning.html")

@app.route("/cleaned")
def mmds():
    from static.PY.cleaning_class import Cleaning
    
    data_cleaned = Cleaning(
        raw_file_path=uploaded_file_path,
        correlation_in_columns=0.49
    )

    image_path = f"{(os.path.splitext(uploaded_file_path)[0]).replace('Downloads','Images')}_distribution.png"
    print(image_path)
    data_cleaned.save_distribution_image(download_image_path=image_path)
    return fl.render_template("views/testing.html",image_path = image_path)

if __name__ == '__main__':
    app.run(debug=True)