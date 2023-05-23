import cv2
import os
from PIL import Image, ImageOps
#this function was based on the one found here: https://towardsdatascience.com/generate-pencil-sketch-from-photo-in-python-7c56802d8acb
def convertToSketch(photo, k_size, greyName, resultName):
    #Opening up the image that we were passed
    img=cv2.imread(photo)
    #Converting the image into greyscale
    imgGrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #saving the grey image (will be used later)
    cv2.imwrite(greyName, imgGrey)
    #Inverting the image and blurring it using gaussian blur
    imgInvt=cv2.bitwise_not(imgGrey)
    imgBlur=cv2.GaussianBlur(imgInvt, (k_size,k_size),0)
    #un-inverting the blurred image
    imgBlurInvt=cv2.bitwise_not(imgBlur)
    #deriving the "pencil sketch" image by dividing the grey image by the blurred one
    imgSketch=cv2.divide(imgGrey,imgBlurInvt, scale=256.0)
    
    # Saving the sketch image
    cv2.imwrite(resultName, imgSketch)
    
#this function alters the coloring of the image using PIL's colorize method
def blueScale(photo):
    #opening up the sketch image
    img =  Image.open(photo, "r")
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

blueSketch = convertToSketch(photo='plains.jpg', k_size=(int(input("What thickness would you like, on a scale of 1-10?\n")) * 20 + 1), greyName = 'grey.png', resultName = 'sketch.png')
bSketch = blueScale(photo='sketch.png')
bPhoto = blueScale(photo='grey.png')

imgOverlay(photo=bSketch, overlay = bPhoto, result = 'result1.png')
os.remove("sketch.png")
os.remove("grey.png")
