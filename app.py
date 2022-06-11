from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
import numpy as np
import os
from flask_dropzone import Dropzone
import lang
import cv2
import helper
import easyocr
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
    kalimatAsal, kalimatTujuan = [], []
    asal = request.form["asal"]
    # tujuan = request.form["tujuan"]
    print(asal)
    asalOcr = lang.LANGUAGES_EASYOCR_ASAL_REVERSE[asal]
    asalTrans = lang.LANGUAGES_TRANSLATE_ASAL_REVERSE[asal]
    tujuanTrans = lang.LANGUAGES_TRANSLATE_TUJUAN_REVERSE['indonesian']
    reader = easyocr.Reader([asalOcr])
    fileNames = os.listdir(dirFull)
    for i in fileNames:
        listPath.append(os.path.abspath(os.path.join(dirFull, i)))
        listFile.append(i)
    err, baseFile, inputFile = helper.cekFormat(listFormat, listFile)
    print(err, baseFile, inputFile)
    pesanError = helper.cekError(error, err)
    print(pesanError)
    if pesanError != None:
        for i in listPath:
            os.unlink(i)
            print(i)
        return (redirect(url_for('fitur1', pesan = pesanError)))
    
    if baseFile == 'gambar':
        for i in listPath:
            img = helper.readImage(i)
            teks = helper.imageToStringEasyOcr(img, reader)

            for i in teks:
                kalimatAsal.append(i)
                i = helper.translate(i, asalTrans, tujuanTrans)
                kalimatTujuan.append(i)
    elif baseFile == 'pdf':
        listImage = helper.pdfToImage(listPath[0])
        for i in listImage:
            img = helper.readImage(i)
            teks = helper.imageToStringEasyOcr(img, reader)

            for i in teks:
                kalimatAsal.append(i)
                i = helper.translate(i, asalTrans, tujuanTrans)
                kalimatTujuan.append(i)
    for i in listPath:
        os.unlink(i)
        print(i)
    return render_template("hasilfitur1.html", asal = kalimatAsal, panjangAsal = len(kalimatAsal), tujuan = kalimatTujuan, panjangTujuan = len(kalimatTujuan))


@app.route("/fitur2")
def fitur2():
    return render_template("fitur2.html")



if __name__ == '__main__':
    app.run(port=5000, debug=True)