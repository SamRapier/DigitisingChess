import cv2
import numpy as np

kernelArr_X = [
                np.array([  [ 1, 1, 1], 
                            [ 0, 0, 0], 
                            [-1,-1,-1]
                        ]),

                np.array([  [-1,-1,-1],
                            [ 0, 0, 0], 
                            [ 1, 1, 1]
                        ])]

kernelArr_Y = [
                np.array([  [-1, 0, 1], 
                            [-1, 0, 1], 
                            [-1, 0, 1]
                        ]),

                np.array([  [ 1, 0,-1], 
                            [ 1, 0,-1], 
                            [ 1, 0,-1]
                        ])]


def applyFilter(image, kernel):
    return cv2.filter2D(image, -1, kernel)

def directionalPrewitt(image, kernelArr):
    return (applyFilter(image, kernelArr[0]) + applyFilter(image, kernelArr[1]))

def prewitt(image):
    prewitt_X = directionalPrewitt(image, kernelArr_X)
    prewitt_Y = directionalPrewitt(image, kernelArr_Y)

    img_prewitt = np.hypot(prewitt_X, prewitt_Y)
    img_prewitt = (img_prewitt / img_prewitt.max() * 255).astype('unit8')

    theta = np.arctan2(prewitt_Y, prewitt_X).astype('uint8')

    return img_prewitt, theta