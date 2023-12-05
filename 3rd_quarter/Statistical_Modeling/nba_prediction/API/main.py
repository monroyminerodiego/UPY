import flask as fl
from werkzeug.utils import secure_filename
import os

app = fl.Flask(__name__,template_folder='static/HTML/')
uploaded_file_path = ''
app.config["UPLOAD_FOLDER"] = 'static/Downloads'

ALLOWED_EXTENSIONS = set(['csv'])

@app.route("/")
def root():
    global uploaded_file_path
    os.system('cls')
    print(f'\n\n\n{"*"*15} Esta en vista root {"*"*15}\n\n\n')
    return fl.render_template('views/index.html')
uploaded_file_path = uploaded_file_path

@app.route("/selected",methods=['POST']) #type: ignore
def selected():
    global uploaded_file_path
    print(f'\n\n\n{"*"*15} Esta en vista selected {"*"*15}\n\n\n')
    if fl.request.method == 'POST':
        file = fl.request.files['Name_UploadFile']
        filename = secure_filename(file.filename) #type: ignore
        uploaded_file_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        file.save(uploaded_file_path)
        column_names = (((open(uploaded_file_path,'r').readline()).replace('\n','')).split(','))
        return fl.render_template("views/cleaning.html",column_names=column_names,file_path=file)

uploaded_file_path = uploaded_file_path

@app.route("/cleaned",methods=['POST'])
def cleaned():
    pct_correlation = fl.request.get_data().split('&')
    os.system('cls')
    print(f'\n\n\n{"*"*15} Esta en vista cleaned {"*"*15}\n{type(pct_correlation)}.- {pct_correlation}\n\n\n')
    from static.PY.cleaning_class import Cleaning
    data_cleaned = Cleaning(
        raw_file_path=uploaded_file_path,#type:ignore
        correlation_in_columns=0.49
    ) 
    image_path = f"{(os.path.splitext(uploaded_file_path)[0]).replace('Downloads','Images')}_distribution.png"
    data_cleaned.save_distribution_image(download_image_path=image_path)
    return fl.render_template("views/testing.html",image_path = image_path)

if __name__ == '__main__':
    app.run(debug=True)