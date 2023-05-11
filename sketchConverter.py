import cv2
from PIL import Image, ImageOps
#this function was based on the one found here: https://towardsdatascience.com/generate-pencil-sketch-from-photo-in-python-7c56802d8acb
def convertToSketch(photo, k_size):
    #Opening up the image that we were passed
    img=cv2.imread(photo)
    #Converting the image into greyscale
    imgGrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Inverting the image and blurring it using gaussian blur
    imgInvt=cv2.bitwise_not(imgGrey)
    imgBlur=cv2.GaussianBlur(imgInvt, (k_size,k_size),0)
    #un-inverting the blurred image
    imgBlurInvt=cv2.bitwise_not(imgBlur)
    #deriving the "pencil sketch" image by dividing the grey image by the blurred one
    imgSketch=cv2.divide(imgGrey,imgBlurInvt, scale=256.0)
    # Saving the sketch image
    cv2.imwrite('sketch.png', imgSketch)
    
def blueScale(photo):
    #opening up the sketch image
    img =  Image.open(photo, "r")
    #utilizing PIL's colorize to change to bluescale
    img = ImageOps.colorize(img, black = "#4c9ccc", white = "#e9ddb3")
    img.show()
#toDo: make it so user can select the image they want to convert
convertToSketch(photo='sunset.jpg', k_size=(int(input("What kernel size would you like? Larger kernels will be more detailed but less sketch-like.\n"))))
blueScale(photo='sketch.png')
