import radon, pre_processing, canny, utils
from pre_processing import blurImage, grayScale, image_resize
from prewitt import prewitt
from canny import cannyAlgo
from radon import radonTransform
import cv2, numpy as np


if __name__ == "__main__":
    testImg = pre_processing.loadImg('testImg/testImg.png')
    testImg = blurImage(grayScale(testImg))

    img_prewitt, theta = prewitt(testImg)

    img_canny = cannyAlgo(img_prewitt, theta)

    sinogram = radonTransform(img_canny)

    stdDev = np.std(sinogram)
    bestLinePoints = utils.applySimpleThreshold(sinogram, 170+stdDev, cv2.THRESH_BINARY)

    

    utils.displayImage(bestLinePoints)