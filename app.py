from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
from flask_dropzone import Dropzone

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_MAX_FILES=30,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='upload_file',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)

dropzone = Dropzone(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fitur1")
def fitur1():
    return render_template("fitur1.html")

@app.route("/", methods=['GET', 'POST'])    
def upload_file():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    else:
        print('gagal')
    return render_template("fitur12.html")


@app.route("/fitur2")
def fitur2():
    return render_template("fitur2.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)