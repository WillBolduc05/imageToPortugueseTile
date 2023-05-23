import cv2
import os
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

def imgOverlay(photo, overlay, result):
    #opening up the images
    img1 = bPhoto
    img2 = bSketch
    #overlaying the overlay onto the photo. The ratio ranges from 0 to 1, where 0 would be entirely the overlay and 1 would be entirely the photo
    img1 = Image.blend(img1,img2, 0.75)
    #saving the image
    img1.save(result)
    img1.show()

ARGPARSER = argparse.ArgumentParser()
ARGPARSER.add_argument("--thickness", type=int)
ARGPARSER.add_argument("--input", type=str)
ARGPARSER.add_argument("--output", type=str)
ARGS = ARGPARSER.parse_args()

blueSketch = convertToSketch(photo=ARGS.input, k_size=(ARGS.thickness * 20 + 1))
bSketch = blueScaleFromGrey(photo=blueSketch)
original = cv2.imread('plains.jpg')
bPhoto = blueScaleFromRGB(photo=original)

imgOverlay(photo=bSketch, overlay = bPhoto, result = ARGS.output)
