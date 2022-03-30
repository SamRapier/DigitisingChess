import cv2
import matplotlib.pyplot as plt
import numpy as np


def applySimpleThreshold(image, threshVal, thresholdType):
    ret,simple_threshold = cv2.threshold(image, threshVal, 255, thresholdType)
    return simple_threshold

def displayImage(image):
    plt.imshow(image, cmap=plt.cm.Greys_r, aspect='auto')


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


def lineOfBestFit(sinogram):
    prevX = 0
    count = 0

    _points = collectPeakPoints

    # colorArr = ['red', 'orange', 'green', 'blue', 'purple', 'yellow', 'black', 'pink']
    lineArr = []
    gradientsArr = []
    xArr = np.array([])
    yArr = np.array([])
    (x,y) = _points[0]

    counter = 0
    while counter < len(_points):
        while x < (prevX+40):
            prevX = x

            xArr = np.append(xArr, x)
            yArr = np.append(yArr, y)
            
            counter += 1

            if counter > (len(_points)-1):
                break

            (x,y) = _points[counter]

        prevX = x
        # get gradient and y-intercept for line of best fit
        m, b = np.polyfit(xArr, yArr, 1)
        gradientsArr.append([m,b])

        # # plot points and lines
        # plt.plot(xArr, m*xArr + b, c=colorArr[count])
        # plt.plot(xArr, yArr, '.', c=colorArr[count])

        lineArr.append([xArr, yArr])
        xArr = np.array([])
        yArr = np.array([])

        count+= 1        
        if count > 7:
            count = 0
    
    return gradientsArr, lineArr





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