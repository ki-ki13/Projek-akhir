from flask import Flask, flash, redirect, render_template, request, jsonify, url_for, send_file
import numpy as np
import os
from flask_dropzone import Dropzone
import lang
import cv2
import helper
import easyocr
from PyPDF2 import PdfFileMerger

listFormat, error = helper.formatAndError()
basedir = os.path.abspath(os.path.dirname(__file__))
dirFull = f'{basedir}\\static\\upload'
dirFullSementara = f'{basedir}\\static\\sementara'
pathHasilPdf=os.path.join(basedir, 'static\\hasilPDF')
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
    fileHasilPDF = os.listdir(pathHasilPdf)
    for i in fileHasilPDF:
        os.unlink(os.path.abspath(os.path.join(pathHasilPdf, i)))
    return render_template("index.html")


@app.route("/fitur1")
def fitur1():
    return render_template('fitur1.html')

@app.route("/fitur1text", methods=['GET','POST'])
def fitur1text():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    pesanError = request.args.get('pesan')
    return render_template('fitur1text.html', foobar=lang.LANGUAGES_EASYOCR_ASAL, foobartujuan = lang.LANGUAGES_TRANSLATE_TUJUAN, pesan=pesanError)

@app.route("/fitur1pdf", methods=['GET','POST'])
def fitur1pdf():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    pesanError = request.args.get('pesan')
    return render_template('fitur1pdf.html', pesan=pesanError)
# @app.route("/fitur1/proses", methods=['POST'])   
# def upload_file():
#     f = request.files.get('file')
#     print(f,f.filename)

@app.route("/fitur1/hasiltext", methods=['POST'])
def hasiltext():
    listFile = []
    listPath = []
    dictAsal, dictTujuan = {},{}
    asal = request.form["asal"]
    tujuan = request.form["tujuan"]
    print(f'Asal bahasa {asal} -> {tujuan}')
    asalOcr = lang.LANGUAGES_EASYOCR_ASAL_REVERSE[asal]
    asalTrans = lang.LANGUAGES_TRANSLATE_ASAL_REVERSE[asal]
    tujuanTrans = lang.LANGUAGES_TRANSLATE_TUJUAN_REVERSE[tujuan]
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
        return (redirect(url_for('fitur1text', pesan = pesanError)))
    
    if baseFile == 'gambar':
        urutan = 0
        for i in listPath:
            kalimatAsal, kalimatTujuan = [], []
            img = helper.readImage(i)
            teks = helper.imageToStringEasyOcr(img, reader)
            urutan += 1

            for i in teks:
                kalimatAsal.append(i)
                i = helper.translate(i, asalTrans, tujuanTrans)
                kalimatTujuan.append(i)
            dictAsal[urutan] = kalimatAsal
            dictTujuan[urutan] = kalimatTujuan
    elif baseFile == 'pdf':
        listImage = helper.pdfToImage(listPath[0])
        urutan = 0
        print('Menjalankan loop')
        for i in listImage:
            print(f'Proses gambar ke-{urutan+1}')
            kalimatAsal, kalimatTujuan = [], []
            img = helper.readImage(i)
            teks = helper.imageToStringEasyOcr(img, reader)
            urutan += 1

            for i in teks:
                kalimatAsal.append(i)
                i = helper.translate(i, asalTrans, tujuanTrans)
                kalimatTujuan.append(i)
            dictAsal[urutan] = kalimatAsal
            dictTujuan[urutan] = kalimatTujuan
            print(f'Gambar ke-{urutan} selesai')
        for i in listImage:
            os.unlink(i)
    for i in listPath:
        os.unlink(i)
    return render_template("hasilfitur1text.html", asal = dictAsal, tujuan = dictTujuan, basefile = baseFile)

@app.route("/fitur1/hasilpdf", methods=['POST'])
def hasilpdf():
    fileHasilPDF = os.listdir(pathHasilPdf)
    for i in fileHasilPDF:
        os.unlink(os.path.abspath(os.path.join(pathHasilPdf, i)))
    
    merger = PdfFileMerger()
    nilai = 0
    listFile = []
    listPath = []
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
        return (redirect(url_for('fitur1pdf', pesan = pesanError)))
    
    if baseFile == 'gambar':
        for i in listPath:
            img = helper.readImage(i)
            merger = helper.saveAndMergePdf(img, nilai, merger)
            nilai += 1
        merger.write(os.path.join(pathHasilPdf,'HasilPDFbaru.pdf'))
        merger.close()

        fileNamesPDF = os.listdir(dirFullSementara)
        for i in fileNamesPDF:
            os.unlink(os.path.abspath(os.path.join(dirFullSementara, i)))

        filePDF = os.listdir(pathHasilPdf)
        for i in filePDF:
            path = os.path.abspath(os.path.join(pathHasilPdf, i))
        print(path)
    
    else:
        listImage = helper.pdfToImage(listPath[0])
        print('Menjalankan loop')
        for i in listImage:
            img = helper.readImage(i)
            merger = helper.saveAndMergePdf(img, nilai, merger)
            nilai += 1
        merger.write(os.path.join(pathHasilPdf,'HasilPDFbaru.pdf'))
        merger.close()
        for i in listImage:
            os.unlink(i)
        fileNamesPDF = os.listdir(dirFullSementara)
        for i in fileNamesPDF:
            os.unlink(os.path.abspath(os.path.join(dirFullSementara, i)))

        filePDF = os.listdir(pathHasilPdf)
        for i in filePDF:
            path = os.path.abspath(os.path.join(pathHasilPdf, i))
        print(path)

    for i in listPath:
        os.unlink(i)
    return render_template("hasilfitur1pdf.html")

@app.route("/download")
def save_file():
    path = os.path.abspath(os.path.join(pathHasilPdf, "HasilPDFbaru.pdf"))
    return send_file(path ,as_attachment=True, cache_timeout=0)


@app.route("/fitur2")
def fitur2():
    return render_template("fitur2.html")



if __name__ == '__main__':
    app.run(port=5000, debug=True)