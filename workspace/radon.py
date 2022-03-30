from skimage.transform import radon, iradon
import numpy as np
import cv2

def calcTheta(image):
    return np.linspace(0., 360., max(image.shape), endpoint=False)

def radonTransform(image):
    return radon(image, theta=calcTheta(image), circle=False)

def filteredBackProjection(sinogram, _theta):
    # theta = np.linspace(0., 360., max(image.shape), endpoint=False)
    return iradon(sinogram, theta=_theta, filter_name='cosine', circle=False)



def collectPeakPoints(sinogram):

    points = []

    for i in range(len(sinogram)):
        for j in range(len(sinogram[0])):
            if sinogram[i][j] > 254:
                points.append([j,i])

    points2 = sorted(points, key=lambda x: x[0])

    points_limited = []
    for i in range(len(points2)):
        if points2[i][1] > 200 and points2[i][1] < 700:
            points_limited.append(points2[i])

    return points_limited




# def calcSecondDeriv():

