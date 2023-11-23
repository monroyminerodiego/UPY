import flask as fl

app = fl.Flask(__name__)

@app.route("/")
def root():
    return fl.render_template("index.html")

@app.route("/add_file",method=['POST'])
def add_file():
    if fl.request.method == 'POST':
        print('Hola')

if __name__ == '__main__':
    app.run(debug=True)