import os
import threading
import flask as fl
from werkzeug.utils import secure_filename
from static.PY.cleaning_class import Cleaning
from static.PY.MLRegression import Multiple_linear_regression

# ==================== Declaration of application ====================  
app = fl.Flask(__name__)


# ==================== Configurations ==================== 
app.config["UPLOAD_FOLDER"]   = 'static/Downloads'
app.template_folder           = 'static/HTML/'


# ==================== Global variables ==================== 
uploaded_file_path            = ''
downloaded_image_path         = ''


# ==================== URL's ==================== 
@app.route("/")
def root():
    os.system('cls')
    return fl.render_template('views/index.html')

uploaded_file_path = uploaded_file_path
downloaded_image_path = downloaded_image_path




@app.route("/selected",methods=['POST']) #type: ignore
def selected():
    global uploaded_file_path
    if fl.request.method == 'POST':
        file = fl.request.files['Name_UploadFile']
        filename = secure_filename(file.filename) #type: ignore
        uploaded_file_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        file.save(uploaded_file_path)
        
        column_names = (((open(uploaded_file_path,'r').readline()).replace('\n','')).split(','))
        
        cheat = threading.Thread(target=default, daemon=True)
        cheat.start()

        return fl.render_template("views/cleaning.html",column_names=column_names,file_name=os.path.split(uploaded_file_path)[1])

uploaded_file_path = uploaded_file_path
downloaded_image_path = downloaded_image_path




@app.route("/cleaned",methods=['POST'])
def cleaned():
    global downloaded_image_path
    downloaded_image_path = f"{(os.path.splitext(uploaded_file_path)[0]).replace('Downloads','Images')}_distribution.png"
    requested_data  = fl.request.form
    variable = requested_data['variables']
    pct_correlation = float(requested_data['pct_correlation'])
    normalize = False
    estandarize = True

    if (variable != 'net_rating') or (pct_correlation != 0.49) or (normalize) or not(estandarize):
        data_cleaned = Cleaning(
            raw_file_path=uploaded_file_path,
            correlation_in_columns=pct_correlation,
            estandarize_data=estandarize,
            normalize_data=normalize
        ) 
        data_cleaned.save_distribution_image(download_image_path=downloaded_image_path,name_dependent_variable=variable)
        
    return fl.render_template("views/testing.html",downloaded_image_path = downloaded_image_path,pct_correlation = pct_correlation)

uploaded_file_path = uploaded_file_path
downloaded_image_path = downloaded_image_path




def default():
    global downloaded_image_path
    
    data_cleaned = Cleaning(
        raw_file_path=uploaded_file_path,
        correlation_in_columns=0.49
    ) 
    
    downloaded_image_path = f"{(os.path.splitext(uploaded_file_path)[0]).replace('Downloads','Images')}_distribution.png"
    data_cleaned.save_distribution_image(download_image_path=downloaded_image_path,name_dependent_variable='net_rating')

uploaded_file_path = uploaded_file_path
downloaded_image_path = downloaded_image_path





# ==================== Debugging = True ==================== 
if __name__ == '__main__':
    app.run(debug=True)