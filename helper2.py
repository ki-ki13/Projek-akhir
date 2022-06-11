# function to convert the JavaScript object into an OpenCV image
import cv2
from base64 import b64decode, b64encode
import lang
import numpy as np
import easyocr

def js_to_image(js_reply):
    # decode base64 image
    image_bytes = b64decode(js_reply.split(',')[1])
    # convert bytes to numpy array
    jpg_as_np = np.frombuffer(image_bytes, dtype=np.uint8)
    # decode numpy array into OpenCV BGR image
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

def inputBahasa(asal,tujuan):
    asal = lang.cek(asal)
    tujuan = lang.cek(tujuan)
    reader = easyocr.Reader([asal])
    return reader, asal, tujuan