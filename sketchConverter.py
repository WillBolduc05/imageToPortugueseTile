from flask import Flask, render_template, request
from PIL import Image
import cv2
import os
import argparse
import numpy
import base64
import io
from PIL import Image, ImageOps

def convertToSketch(photo, k_size):
    #Opening up the image that we were passed
    img = numpy.array(photo)  
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #Converting the image into greyscale
    imgGrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #saving the grey image (will be used later)
    #Inverting the image and blurring it using gaussian blur
    imgInvt=cv2.bitwise_not(imgGrey)
    imgBlur=cv2.GaussianBlur(imgInvt, (k_size,k_size),0)
    #un-inverting the blurred image
    imgBlurInvt=cv2.bitwise_not(imgBlur)
    #deriving the "pencil sketch" image by dividing the grey image by the blurred one
    imgSketch=cv2.divide(imgGrey,imgBlurInvt, scale=256.0)
    return imgSketch
    
#this function alters the coloring of the image using PIL's colorize method
def blueScaleFromGrey(photo):
    #opening up the sketch image
    img = Image.fromarray(photo)
    #utilizing PIL's colorize to change to bluescale
    img = ImageOps.colorize(img, black = "#4c9ccc", white = "#e9ddb3")
    #img.show()
    return img

def blueScaleFromRGB(photo):
    #opening up the sketch image
    imgGrey=cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(imgGrey)
    #utilizing PIL's colorize to change to bluescale
    img = ImageOps.colorize(img, black = "#4c9ccc", white = "#e9ddb3")
    #img.show()
    return img

def imgOverlay(photo, overlay):
    #opening up the images
    img1 = overlay
    img2 = photo
    #overlaying the overlay onto the photo. The ratio ranges from 0 to 1, where 0 would be entirely the overlay and 1 would be entirely the photo
    img1 = Image.blend(img1,img2, 0.75)
    return img1

def drawTiles(photo, xLines, yLines, thickness, result):
    cvPhoto = numpy.array(photo)  
    cvPhoto = cv2.cvtColor(cvPhoto, cv2.COLOR_RGB2BGR)
    color = (200, 200, 200)
    h, w, channels = cvPhoto.shape
    xStep = w / (xLines)
    yStep = h / (yLines)
    for i in range(1,xLines):
        x = xStep * i
        startPoint = (int(x),int(0))
        endPoint = (int(x),int(h))
        cv2.line(cvPhoto, startPoint,endPoint,color,thickness)
    for i in range(1,yLines):
        y = yStep * i
        startPoint = (int(0),int(y))
        endPoint = (int(w),int(y))
        cv2.line(cvPhoto, startPoint, endPoint,color,thickness)
    return cvPhoto
def convertImage(photo, thickness = 1, xTiles = 4, yTiles = 4, tileThickness = 1):
        blueSketch = convertToSketch(photo=photo, k_size=(thickness * 20 + 1))
        bSketch = blueScaleFromGrey(photo=blueSketch)
        img1 = numpy.array(photo)  
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
        bPhoto = blueScaleFromRGB(photo=img1)
        overlayPhoto = imgOverlay(photo=bSketch, overlay = bPhoto)
        output = drawTiles(photo=overlayPhoto, xLines = xTiles, yLines = yTiles, thickness = tileThickness, result = "output.png")
        outputStep1 = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        PILOutput = Image.fromarray(outputStep1)
        return PILOutput



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    image = request.files['file']
    img = Image.open(image)
    img = numpy.array(img)
    
    output = convertImage(photo = img, thickness = 1, xTiles = 4, yTiles = 4, tileThickness = 2)
    newsize = (500, 500)
    smallOutput = output.resize(newsize)
    data = io.BytesIO()
    smallOutput.save(data, "JPEG")
    small_encoded_img_data = base64.b64encode(data.getvalue())
    data1 = io.BytesIO()
    output.save(data1, "JPEG")
    encoded_img_data = base64.b64encode(data1.getvalue())

    return render_template('image.html', msg='Here is the tile version of your image! Enjoy!', img_data=encoded_img_data.decode('utf-8'), small_img_data=small_encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port ="8000")
