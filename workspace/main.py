import radon, pre_processing, utils
from pre_processing import blurImage, grayScale, image_resize
from prewitt import prewitt
from canny import cannyAlgo
from radon import radonTransform
import cv2, numpy as np
import line_detector
from config import *
import intersection_detector
import debug


if __name__ == "__main__":
    testImg = pre_processing.loadImg('testImg/testImg.png')
    testImg = image_resize(blurImage(grayScale(testImg)))
    debug.image(testImg.astype('uint8')).save("testImg")

    # pad image here
    # pad img_canny with zeros so its square
    paddedImg = utils.padToSquare(testImg)
    debug.image(paddedImg.astype('uint8')).save("paddedImg")


    img_prewitt, theta = prewitt(paddedImg)
    debug.image(img_prewitt.astype('uint8')).save("prewitt_transform")

    img_canny = cannyAlgo(img_prewitt, theta)
    debug.image(img_canny.astype('uint8')).save("canny_transform")




    sinogram = radonTransform(img_canny)
    debug.image(sinogram.astype('uint8')).save("sinogram")


    stdDev = np.std(sinogram)
    bestLinePoints = utils.applySimpleThreshold(sinogram, 150+stdDev, cv2.THRESH_BINARY)
    debug.image(bestLinePoints.astype('uint8')).save("bestLinePoints")
   

    secondDerivative = radon.calcSecondDeriv(bestLinePoints)
    debug.image(secondDerivative.astype('uint8')).save("secondDerivative")

    theta = radon.calcTheta(img_canny)
    gridLayout = radon.filteredBackProjection(secondDerivative, theta)
    gridLayout = utils.applySimpleThreshold(gridLayout, 0.015, cv2.THRESH_BINARY)

    # utils.displayImage(gridLayout)
    debug.image(gridLayout.astype('uint8')).save("gridLayout")


    segments = line_detector.slid_detector(gridLayout.astype('uint8'))

    rawLines = line_detector.SLID(gridLayout, segments)
    debug.image(paddedImg.astype('uint8')).lines(rawLines, size=2).save("rawLines_on_testImg")

    lines = line_detector.slid_tendency(rawLines)
    debug.image(paddedImg.astype('uint8')).lines(lines, size=2).save("lines_on_testImg")

    points = intersection_detector.intersections(lines)
    debug.image(gridLayout.astype('uint8')).points(points, size=3).save("laps_in_queue")
    debug.image(paddedImg.astype('uint8')).points(points, size=3).save("intersections_on_testImg")


    # may need to scale intersections to plot them back onto original image rather than gridLayout

    # convert points back to a numpy array and then perform a radon transform on this
    pointsImg = utils.buildNumpyArray(points, gridLayout)

    # perform radon transform on pointsImg
    intersection_Rspace = radonTransform(pointsImg)
    intersection_Rspace = utils.applySimpleThreshold(intersection_Rspace, 150, cv2.THRESH_BINARY)
    # utils.displayImage(intersection_Rspace)


    print(len(points), len(pointsImg))