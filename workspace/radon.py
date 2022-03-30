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

def applyBoundaries(image, arrGradient, arrLines, padding):
	xArr, yArr = getLineBestFit(image.shape[0], arrGradient, arrLines)
	newImage = np.zeros(image.shape, image.dtype)

	for j in range(image.shape[0]):
		for i in range(image.shape[1]):
			
			# i is essentially y-1
			# if i == 180:
				# print(i)
			if (i > (xArr[1][j] + padding) and (i < xArr[2][j] - padding)) or (i > (xArr[2][j] + padding) and (i < xArr[3][j] - (padding+1))):
				newImage[j][i] = image[j][i]	

			# if (x > (lineArr[1][i] + padding) and x < (xArr[y][x] - padding)):

			# if (x > xArr[2][x] and x < xArr[3][x]):
			# 	newImage[y][x] = image[y][x]	

	return newImage			


def calcSecondDeriv():
	# betterSecondDeriv
	# take the lowest y and x coord that sits on the green and red line

	# use equation of green and red line to find x coord at lowest and max height
	# set value of points outside these bounds to zero

	secDerivExtract = np.zeros(betterSecondDeriv.shape)

	m = 0
	c = 0
	xMin_1 = 0
	xMin_2 = 0
	xMax_1 = 0
	xMax_2 = 0

	yMin = 200
	yMax = 800

	# plt.imshow(image, cmap=plt.cm.Greys_r, aspect='auto')
	# plt.imshow(bestLinePoints,'gray',vmin=0,vmax=255, aspect='auto')

	def getX(y, m, c):
	return (y-c) / m

	def withinBounds(x, y):
	#   xMin_1 = getX(yMax, gradientsArr[2][0], gradientsArr[2][1])
	#   xMax_1 = getX(yMax, gradientsArr[2][0], gradientsArr[2][1])
	#   xMin_2 = getX(yMax, gradientsArr[3][0], gradientsArr[3][1])
	#   xMax_2 = getX(yMax, gradientsArr[3][0], gradientsArr[3][1])

	if (x > 300 and y > 200) and (x < 550 and y < 800):
		return True
	else:
		return False 

	# for (x,y) in betterSecondDeriv:

	print("i: 0-", len(betterSecondDeriv))
	print("j: 0-", len(betterSecondDeriv[0]))

	for i in range(len(betterSecondDeriv)):
	for j in range(len(betterSecondDeriv[0])):
		if withinBounds(j, i):
		secDerivExtract[i][j] = betterSecondDeriv[i][j]

	print(len(secDerivExtract))

