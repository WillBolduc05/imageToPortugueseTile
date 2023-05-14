import cv2
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
def blueScale(photo, bluePhoto):
    #opening up the sketch image
    img =  Image.open(photo, "r")
    #utilizing PIL's colorize to change to bluescale
    img = ImageOps.colorize(img, black = "#4c9ccc", white = "#e9ddb3")
    #img.show()
    img.save(bluePhoto)\

#this function combines the blueSketch with a blueScaled version of the original to add more background elements
def imgOverlay(photo, overlay, result):
    #opening up the images
    img2 = Image.open(photo).convert("RGBA")
    img1 = Image.open(overlay).convert("RGBA")
    #overlaying the overlay onto the photo. The ratio ranges from 0 to 1, where 0 would be entirely the overlay and 1 would be entirely the photo
    img1 = Image.blend(img1,img2, 0.75)
    #saving the image
    img1.save(result)
    img1.show()

convertToSketch(photo='knights.jpg', k_size=(int(input("What kernel size would you like? Larger kernels will be more detailed but less sketch-like.\n"))), greyName = 'grey.png', resultName = 'sketch.png')
blueScale(photo='sketch.png', bluePhoto='blueSketch.png')
blueScale(photo='grey.png', bluePhoto='bluePhoto.png')
imgOverlay(photo='blueSketch.png', overlay = 'bluePhoto.png', result = 'result.png')
