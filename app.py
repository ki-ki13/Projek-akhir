from csv import reader
from flask import Flask, render_template, request, session
from flask_session import Session
import joblib
import numpy as np
import cv2
import os
import helper2
import lang
from flask_dropzone import Dropzone
from base64 import b64decode

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_MAX_FILES=30,
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    # DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='fitur1',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)

dropzone = Dropzone(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fitur1",methods=['GET','POST'])
def fitur1():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    pesanError = request.args.get('pesan')
    return render_template('fitur1.html', foobar=lang.LANGUAGES, pesan=pesanError)

@app.route("/fitur1/hasil", methods=['POST'])   
def upload_file():
    asal0 = request.form.get('asal')
    tujuan = request.form.get('tujuan')
    asal2 = request.form.get('asal2')
    asal = lang.cek(asal2)
    hasil = []
    # photo = ""
    print(asal,tujuan)
        # photo = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        # photo = readImage(photo)
        # lis = hasil
        # lis.append(photo)
        # hasil = lis
        # print(photo, "-", hasil)
        # photo = helper.imageToStringEasyOcr(photo,'en')
        # print(key,photo)
        # hasil.append(photo)
    return render_template("fitur12.html", foobar = lang.LANGUAGES, asal= asal0,tujuan=tujuan)


@app.route("/fitur2")
def fitur2():
    return render_template("bahasa.html", foobar=lang.LANGUAGES)

@app.route("/inputbahasa",methods=["POST"])
def inputbahasa():
    form_data = request.form
    session['reader'],session['asal'],session['tujuan'] = helper2.inputBahasa(form_data['asal'],form_data['tujuan'])
    return render_template('fitur2.html', asal=session['asal'],tujuan=session['tujuan'])

@app.route('/submit',methods=['GET','POST'])
def submit():
    reader = session['reader']
    image = request.args.get('image')
    img = b64decode(image.split(',')[1])
    img = np.frombuffer(img, dtype=np.uint8)
    img = cv2.imdecode(img, flags=1)
    print(type(img))
    # img = helper2.js_to_image(image)
    # result = reader.readtext(img)
    # print(result)
    return ""

if __name__ == '__main__':
    app.run(port=5000, debug=True)