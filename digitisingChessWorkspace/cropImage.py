import cv2
import numpy as np

# take image size
# divide image width by 8 - this is the width of each square
# divide image height by 8 - this is the height of each square

# traverse image by width and height, saving each individual square as we go
# assume looking from white's perspective


# load image

# def loadImg(filename):
# 	"""Load image into memory"""
# 	return cv2.imread(filename)
def gridSegmentation(imageFilePath):
    image = cv2.imread(imageFilePath)


    # get size of image
    imgWidth = image.shape[0]
    imgHeight = image.shape[1]

    stepSizeWidth = int(imgWidth/8)
    stepSizeHeight = int(imgHeight/8)

    # loop through image 
    square_num = 0
    rankCounter = 7
    fileCounter = 0
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = [1, 2, 3, 4, 5, 6, 7, 8]
    for x in range(0, imgWidth, stepSizeWidth):
        for y in range(0, imgHeight, stepSizeHeight):
            # crop image at x, y - save them into a folder with labeled positions
            square = image[y:y+stepSizeHeight, x:x+stepSizeWidth]
            cv2.imwrite('outputs/chessSquares/{}{}.jpg'.format(files[fileCounter], ranks[rankCounter]), square)
            rankCounter -= 1
            square_num += 1
        rankCounter = 7
        fileCounter += 1


# fin
