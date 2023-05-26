import cv2
import os
import argparse
import numpy
from PIL import Image, ImageOps
#this function was based on the one found here: https://towardsdatascience.com/generate-pencil-sketch-from-photo-in-python-7c56802d8acb
def convertToSketch(photo, k_size):
    #Opening up the image that we were passed
    img=cv2.imread(photo)
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
    img1 = bPhoto
    img2 = bSketch
    #overlaying the overlay onto the photo. The ratio ranges from 0 to 1, where 0 would be entirely the overlay and 1 would be entirely the photo
    img1 = Image.blend(img1,img2, 0.75)
    return img1

def drawTiles(photo, xLines, yLines, thickness, result):
    cvPhoto = numpy.array(photo)  
    cvPhoto = cv2.cvtColor(cvPhoto, cv2.COLOR_RGB2BGR)
    color = (99, 108, 122)
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
    cv2.imwrite(result,cvPhoto)

ARGPARSER = argparse.ArgumentParser()
ARGPARSER.add_argument("--thickness", type=int, default = 5, help="This is an integer 1-10 specifying how thick the lines of the drawing will be.")
ARGPARSER.add_argument("--input", type=str, default = "", help = "This should be the address of the image you would like to use as a base.")
ARGPARSER.add_argument("--output", type=str, default = "", help = "This should be the name of the file you would like to have as a result of this program")
ARGPARSER.add_argument("--xTiles", type=int, default = 4, help="This is an integer specifying the number of horizontal tiles.")
ARGPARSER.add_argument("--yTiles", type=int, default = 4, help="This is an integer specifying the number of vertical tiles.")
ARGPARSER.add_argument("--tileThickness", type=int, default = 2, help="This is an integer  how thick the lines of the splits between tiles will be.")

ARGS = ARGPARSER.parse_args()

if (ARGS.input == "" or ARGS.output== ""):
    print("It appears that you have accidentally ommitted the input or output parameter. Those are neccessary for this program to run! If you are confused about the parameters, please run this program with the -h parameter")
else :
    blueSketch = convertToSketch(photo=ARGS.input, k_size=(ARGS.thickness * 20 + 1))
    bSketch = blueScaleFromGrey(photo=blueSketch)
    original = cv2.imread(ARGS.input)
    bPhoto = blueScaleFromRGB(photo=original)
    overlayPhoto = imgOverlay(photo=bSketch, overlay = bPhoto)
    drawTiles(photo=overlayPhoto, xLines = ARGS.xTiles, yLines = ARGS.yTiles, thickness = ARGS.tileThickness, result = ARGS.output)
    
