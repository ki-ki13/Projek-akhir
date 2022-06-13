import cv2
import numpy as np
import sys
import os
import easyocr

from googletrans import Translator
from fpdf import FPDF
from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger
import pytesseract

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_PATH_SEMENTARA=os.path.join(basedir, 'static\\sementara')

#Mengecek format

direction = 'uploads/image/'

def formatAndError():
  listFormat = ['jpg', 'png', 'jpeg', 'pdf']
  error = {1:'Hanya menerima 1 file pdf', 2:'format tidak didukung'}
  return listFormat, error

def cekFormat(listFormat, inputFile):
  err = 0
  listFile = {}
  baseFile = ''
  for i in inputFile:
    i = i.split('.')
    judul, format = i[0], i[1]
    if format in listFormat:
      if format == 'pdf':
        if len(inputFile) >1:
          err = 1
          break
        baseFile = "pdf"
      else:
        baseFile = 'gambar'
      listFile.update({judul: format})
    else:
      err = 2
      break
  return err, baseFile, inputFile

def cekError(error, err):
  if err != 0:
    pesanError = error[err]
    # sys.exit(error[err])
  else:
    pesanError = None
  return pesanError

#Ke PDF
def readImage(path):
    imgori = cv2.imread(path)
    img = cv2.cvtColor(imgori, cv2.COLOR_BGR2RGB)
    return img

def saveAndMergePdf(img, nilai, merger):
    pdf = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
    with open(os.path.join(UPLOADED_PATH_SEMENTARA, f'pdf{nilai}.pdf'), 'w+b') as f:
      f.write(pdf)
    print(os.path.join(UPLOADED_PATH_SEMENTARA, f'pdf{nilai}.pdf'))
    merger.append(os.path.join(UPLOADED_PATH_SEMENTARA, f'pdf{nilai}.pdf'))
    return merger

def pdfToImage(path):
  img = convert_from_path(path)
  listImage = []
  for i in range(len(img)):
    img[i].save(os.path.join(UPLOADED_PATH_SEMENTARA,'page'+ str(i) +'.jpg'))
    print(os.path.join(UPLOADED_PATH_SEMENTARA,'page'+ str(i) +'.jpg'))
    # img[i].save('page'+ str(i) +'.jpg', 'JPEG')
    listImage.append(os.path.join(UPLOADED_PATH_SEMENTARA,'page'+ str(i) +'.jpg'))
  return listImage

def translate(text, asal, tujuan):
  translator = Translator()
  if asal == None:
    translate_text = translator.translate(text, dest=tujuan)
  else:
    translate_text = translator.translate(text, src=asal, dest=tujuan)
  return translate_text.text

#Easy OCR
def imageToStringEasyOcr(img, reader):
  teks = reader.readtext(img, paragraph = True)
  tulisan = []
  for i in teks:
    tulisan.append(i[1])
  return tulisan

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10
    return 1