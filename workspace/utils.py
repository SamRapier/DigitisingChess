import cv2
import matplotlib.pyplot as plt
import numpy as np
import radon


def applySimpleThreshold(image, threshVal, thresholdType):
    ret,simple_threshold = cv2.threshold(image, threshVal, 255, thresholdType)
    return simple_threshold

def displayImage(image):
    plt.imshow(image, cmap=plt.cm.Greys_r, aspect='auto')
    plt.show()


def findPeaks(matrix):
    localPeaks = []

    for i in range(1, (len(matrix) -1)):
        for j in range(1, (len(matrix[0]) -1)):        
            # for each element, if it is greater than all its neighbours, add it to list

            # check vertical neighbours first
            if (compareNeighbours(matrix, i, j, 3)):
                localPeaks.append([j,i])

    return localPeaks

def compareNeighbours(matrix, x, y, radius = 3):
    for i in range(1, radius+1):
        if not ((matrix[x][y] > matrix[x][y+i]) and (matrix[x][y] > matrix[x][y-i]) and (matrix[x][y] > matrix[x+i][y]) and (matrix[x][y] > matrix[x-i][y]) and (matrix[x][y] > matrix[x+i][y+i]) and (matrix[x][y] > matrix[x-i][y+i]) and (matrix[x][y] > matrix[x-i][y-i])and (matrix[x][y] > matrix[x+i][y-i])):
            return False
                       
    return True


def getLineBestFit(yRange, arrGradient):
	m = 0
	c = 0
	xArr = []
	yArr = []
	

	for i in range(yRange):
		yArr.append(i)

	for j in range(len(arrGradient)):
		m,c = arrGradient[j]
		xArr.append([])
		for i in range(yRange):
			xArr[j].append((i - c)/m)

	return (xArr, yArr)


def drawLinesOntop(image, arrGradient, arrLines):

	
	xArr, yArr = getLineBestFit(image.shape[0], arrGradient, arrLines)

	plt.imshow(image, cmap=plt.cm.Greys_r, aspect='auto')
	# plt.imshow(bestLinePoints,'gray',vmin=0,vmax=255, aspect='auto')

	for i in range(len(arrGradient)):
		plt.plot(xArr[i], yArr)


	plt.show()