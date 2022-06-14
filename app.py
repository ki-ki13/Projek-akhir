from flask import Flask, render_template,send_file, request, session,redirect,url_for,jsonify
from flask_session import Session
import numpy as np
from fpdf import FPDF
import cv2
import os
import helper2
import lang
import easyocr
from PIL import Image
from flask_dropzone import Dropzone
from base64 import b64decode

app = Flask(__name__)

listFormat, error = helper2.formatAndError()
basedir = os.path.abspath(os.path.dirname(__file__))
dirFull = f'{basedir}\\static\\upload'
dircam = f'{basedir}\\static\\cam'
global imgl
global t_teks
global deteksi, probab

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"



app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static\\upload'),
    DROPZONE_MAX_FILE_SIZE=1024,
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf'
)

Session(app)
dropzone = Dropzone(app)


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
    listFile = []
    listPath = []
    dictAsal, dictTujuan = {},{}
    kalimatAsal, kalimatTujuan = [], []
    asal = request.form.get('asal')
    tujuan = request.form.get('tujuan')
    asal = lang.cek(asal)
    reader = easyocr.Reader([asal])
    fileNames = os.listdir(dirFull)
    for i in fileNames:
        listPath.append(os.path.abspath(os.path.join(dirFull, i)))
        listFile.append(i)
    err, baseFile, inputFile = helper2.cekFormat(listFormat, listFile)
    print(err, baseFile, inputFile)
    pesanError = helper2.cekError(error, err)
    print(pesanError)
    if pesanError != None:
        for i in listPath:
            os.unlink(i)
            print(i)
        return (redirect(url_for('fitur1', pesan = pesanError)))
    if baseFile == 'gambar':
        urutan = 0
        for i in listPath:
            kalimatAsal, kalimatTujuan = [], []
            img = helper2.readImage(i)
            teks = helper2.imageToStringEasyOcr(img, reader)
            urutan += 1

            for j in teks:
                kalimatAsal.append(j)
                j = helper2.translate(j, asal, tujuan)
                kalimatTujuan.append(j)
            dictAsal[urutan] = kalimatAsal
            dictTujuan[urutan] = kalimatTujuan

    elif baseFile == 'pdf':
        listImage = helper2.pdfToImage(listPath[0])
        urutan = 0
        for i in listImage:
            print(f'Proses gambar ke-{urutan+1}')
            kalimatAsal, kalimatTujuan = [], []
            img = helper2.readImage(i)
            teks = helper2.imageToStringEasyOcr(img, reader)
            urutan += 1

            for i in teks:
                kalimatAsal.append(i)
                i = helper2.translate(i, asal, tujuan)
                kalimatTujuan.append(i)
            dictAsal[urutan] = kalimatAsal
            dictTujuan[urutan] = kalimatTujuan
    for i in listPath:
        os.unlink(i)
        print(i)
    return render_template("fitur12.html",  asal = dictAsal, tujuan = dictTujuan, basefile = baseFile)


@app.route('/download', methods=['POST'])
def save_file():
    texts = request.form.getlist("hasilter[]")
    texts = "\n".join(texts)
    # print(texts)
    # for text in texts.split("\n"):
    #     print(text)
    pdf = FPDF('P', 'cm', 'A4')
    pdf.set_margins(3, 3, 3)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for text in texts.split("\n"):
        pdf.multi_cell(0, 1.15, text.encode('utf-8').decode('latin-1'), 0, 1)
    pdf.output('extracted_text.pdf', 'F')
    return send_file("extracted_text.pdf",as_attachment=True, cache_timeout=0)



@app.route("/fitur2")
def fitur2():
    return render_template("bahasa.html", foobar=lang.LANGUAGES)

@app.route("/inputbahasa",methods=["POST"])
def inputbahasa():
    form_data = request.form
    session['asal'],session['tujuan'] = helper2.inputBahasa(form_data['asal'],form_data['tujuan'])
    return render_template('fitur2.html', asal=session['asal'],tujuan=session['tujuan'])

@app.route('/submit',methods=['GET','POST'])
def submit():
    asal = request.args.get('asal')
    tujuan = request.args.get('tujuan')
    asal, tujuan = helper2.inputBahasa(asal,tujuan)
    # asal = session['asal']
    # tujuan = session['tujuan']
    reader = easyocr.Reader([asal])
    image = request.args.get('image')
    s = image.split(',')[1]
    s = s.replace(" ","+")
    # print(type(s))
    # print(s)
    imgl = b64decode(s)
    # filename = os.path.join(dircam,'some_image.jpeg')  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(img)
    imgl = np.frombuffer(imgl, dtype=np.uint8)
    imgl = cv2.imdecode(imgl, flags=1)
    print(type(imgl))
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
    imgl = cv2.filter2D(src=imgl, ddepth=-1, kernel=kernel)
    # img = helper2.js_to_image(image)
    result = reader.readtext(imgl)
    for (bbox, text, prob) in result:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        text = helper2.translate(text, asal, tujuan)
        imgl = cv2.rectangle(imgl, tl, br, (0, 255, 0), 2)
        imgl = cv2.putText(imgl, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, helper2.get_optimal_font_scale(text, br[0] - tl[0]), (255, 0, 0), 2)
    print(type(imgl))
    t_teks = ""
    deteksi = ""
    probab = ""
    if len(result) > 1:
        for (a, b, c) in result:
            t_teks = t_teks + " " + helper2.translate(b, asal, tujuan)
            deteksi = deteksi + " " + b
            probab = probab + " " + str(c)
            print(f'Kata yang terdeteksi adalah {b} -> {t_teks}, dengan probabilitas {c}')
        print(deteksi)
        print(probab)
    else:
        t_teks = helper2.translate(result[0][1], asal, tujuan)
        deteksi = result[0][1]
        probab = str(result[0][2])
        print(f'Kata yang terdeteksi adalah {result[0][1]} -> {t_teks}, dengan probabilitas {result[0][2]}')
    # img = Image.fromarray(arr.astype('uint8'))
    # file_object = io.BytesIO()   # create file in memory 
    # img.save(file_object, 'PNG') # save PNG in file in memory
    # file_object.seek(0)
    photodir = os.path.join(dircam,'photo.jpeg')
    cv2.imwrite(photodir, imgl)
    # print(result)
    return jsonify({'redirect': url_for("display", teks = t_teks, deteksi=deteksi,probab=probab )})


@app.route('/display/<teks>/<deteksi>/<probab>',methods=['GET'])
def display(teks, deteksi,probab ):
    trans = teks
    hasil_deteksi = deteksi.strip().split(" ")
    hasil_trans = trans.strip().split(" ")
    probab = probab.strip().split(" ")
    len_hasil = len(hasil_deteksi)
    
    return render_template('fitur2.html', trans = trans, hasil_deteksi=hasil_deteksi,len_hasil = len_hasil, hasil_trans = hasil_trans, probab = probab)



@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/howitwork")
def howitwork():
    return render_template("about_us.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)