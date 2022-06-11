from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
import numpy as np
import os
from flask_dropzone import Dropzone
import lang
import cv2
import helper
listFormat, error = helper.formatAndError()
basedir = os.path.abspath(os.path.dirname(__file__))
dirFull = f'{basedir}\\static\\upload'
app = Flask(__name__)


app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static\\upload'),
    DROPZONE_MAX_FILE_SIZE=1024,
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf'
)

dropzone = Dropzone(app)

def readImage(path):
    imgori = cv2.imread(path)
    img = cv2.cvtColor(imgori, cv2.COLOR_BGR2RGB)
    return img

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fitur1", methods=['GET','POST'])
def fitur1():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    pesanError = request.args.get('pesan')
    return render_template('fitur1.html', foobar=lang.LANGUAGES_EASYOCR_ASAL, pesan=pesanError)


# @app.route("/fitur1/proses", methods=['POST'])   
# def upload_file():
#     f = request.files.get('file')
#     print(f,f.filename)

@app.route("/fitur1/hasil", methods=['POST'])
def hasil():
    listFile = []
    listPath = []
    asal = request.form["asal"]
    print(asal)
    fileNames = os.listdir(dirFull)
    for i in fileNames:
        listPath.append(os.path.abspath(os.path.join(dirFull, i)))
        listFile.append(i)
    err, baseFile, inputFile = helper.cekFormat(listFormat, listFile)
    print(err, baseFile, inputFile)
    pesanError = helper.cekError(error, err)
    print(pesanError)
    if pesanError != None:
        return (redirect(url_for('fitur1', pesan = pesanError)))
    return asal


@app.route("/fitur2")
def fitur2():
    return render_template("fitur2.html")



if __name__ == '__main__':
    app.run(port=5000, debug=True)