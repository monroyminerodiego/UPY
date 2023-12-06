import os, threading, flask as fl, pandas as pd, numpy as np, json
from werkzeug.utils import secure_filename
from static.PY import cleaning_class, regression_class

# ==================== Declaration of application ====================  
app = fl.Flask(__name__)


# ==================== Configurations ==================== 
app.config["UPLOAD_FOLDER"] = 'static/Downloads'
app.template_folder         = 'static/HTML/'


# ==================== Global variables ==================== 
uploaded_file_path    = ''
downloaded_image_path = ''
independent_variables = ''
dependent_variable    = ''
pct_correlation       = ''
data_cleaned          = cleaning_class.Cleaning
model                 = regression_class.MLRegression


# ==================== URL's ==================== 
@app.route("/")
def root():
    os.system('cls')
    return fl.render_template('views/index.html')


@app.route("/selected",methods=['POST']) #type: ignore
def selected():
    if fl.request.method == 'POST':
        # === Variables ===
        global uploaded_file_path

        file                    = fl.request.files['Name_UploadFile']
        filename                = secure_filename(file.filename) #type: ignore
        uploaded_file_path      = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        column_names            = (((open(uploaded_file_path,'r').readline()).replace('\n','')).split(','))
        default_behavour_thread = threading.Thread(target=default_cleaning, daemon=True)
        
        # === Calling of methods / classes ===
        file.save(uploaded_file_path)
        default_behavour_thread.start()

        # === Output ===
        return fl.render_template("views/cleaning.html",column_names=column_names,file_name=os.path.split(uploaded_file_path)[1])


@app.route("/cleaned",methods=['POST']) #type:ignore
def cleaned():
    if fl.request.method == 'POST':
        # === Variables ===
        global model
        global independent_variables
        global dependent_variable
        global downloaded_image_path
        global data_cleaned
        global pct_correlation

        requested_data        = fl.request.form
        dependent_variable    = requested_data['variables']
        pct_correlation       = float(requested_data['pct_correlation'])
        try:
            normalize             = True if requested_data['normalizacion']   == 'on' else False
        except:
            normalize             = False
        try:
            estandarize           = True if requested_data['estandarizacion'] == 'on' else False
        except:
            estandarize           = False

        # === Calling of methods / classes ===
        if (dependent_variable != 'net_rating') or (pct_correlation != 0.49) or (normalize) or not(estandarize):
            downloaded_image_path = os.path.split(os.path.splitext(uploaded_file_path.replace('Downloads','Images'))[0])
            downloaded_image_path = f"{downloaded_image_path[0]}/(Modified){downloaded_image_path[1]}_distribution.png"
            
            data_cleaned = cleaning_class.Cleaning(
                raw_file_path          = uploaded_file_path,
                correlation_in_columns = pct_correlation,
                estandarize_data       = estandarize,
                normalize_data         = normalize,
                download_mode          = True,
                cleaned_file_path      = f"{app.config['UPLOAD_FOLDER']}/(Modified)",
                # verbose                = True,
            ) 

            data_cleaned.save_distribution_image(
                download_image_path     = downloaded_image_path,
                name_dependent_variable = dependent_variable
            )

            independent_variables = list(data_cleaned.clean_data_df.columns)
            independent_variables.remove(dependent_variable)

        data_cleaned = data_cleaned
        ordered_titles_list = list(independent_variables) 
        ordered_titles_list.insert(0,dependent_variable)
        basic_list = data_cleaned.clean_data_df[ordered_titles_list] #type:ignore
        basic_list = list(np.array(basic_list))

        model = regression_class.MLRegression(
                basic_list = basic_list
            )

        # === Output ===
        return fl.render_template(
            "views/testing.html",
            downloaded_image_path = downloaded_image_path,
            pct_correlation       = pct_correlation,
            independent_varibles  = list(independent_variables),
            prediction            = 'nada'
        )


@app.route("/predict", methods=['POST']) #type:ignore
def predict():
    # === Variables ===
    data = fl.request.form
    pred = False
    for datita in data:
        if 'x' in datita:
            pred = True
            break

    # === Calling of methods / classes ===
    
    if pred:
        prediction = model.predict([[float(data['x1']),float(data['x2']),float(data['x3']),float(data['x4'])]]) #type:ignore
    else:
        prediction = 'nada'
        print(f'\n\n\n  Tu puto culo\n\n\n')
    

    # === Output ===
    return fl.render_template(
        "views/display.html",
        downloaded_image_path = downloaded_image_path,
        pct_correlation       = pct_correlation,
        independent_varibles  = list(independent_variables),
        prediction            = prediction
    )





def default_cleaning():
    # === Variables ===
    global downloaded_image_path
    global data_cleaned
    global independent_variables

    downloaded_image_path = os.path.split(os.path.splitext(uploaded_file_path.replace('Downloads','Images'))[0])
    downloaded_image_path = f"{downloaded_image_path[0]}/(Default){downloaded_image_path[1]}_distribution.png"

    # === Calling of methods / classes ===
    data_cleaned = cleaning_class.Cleaning(
        raw_file_path          = uploaded_file_path,
        correlation_in_columns = 0.49,
        download_mode          = True,
        cleaned_file_path      = f"{app.config['UPLOAD_FOLDER']}/(Default)",
        # verbose                = True,
    )

    data_cleaned.save_distribution_image(
            download_image_path     = downloaded_image_path,
            name_dependent_variable = 'net_rating'
        )
    
    independent_variables = list(data_cleaned.clean_data_df.columns)
    independent_variables.remove('net_rating')

    # === Output ===
    data_cleaned.save_distribution_image(download_image_path=downloaded_image_path,name_dependent_variable='net_rating')




# ==================== Debugging = True ==================== 
if __name__ == '__main__':
    app.run(debug=True)