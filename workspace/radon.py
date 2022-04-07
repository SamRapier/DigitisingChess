from skimage.transform import radon, iradon
import numpy as np
import utils

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


def lineOfBestFit(sinogram):
	prevX = 0
	count = 0

	_points = collectPeakPoints(sinogram)

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


def applyBoundaries(image, arrGradient, padding):
	xArr, _ = utils.getLineBestFit(image.shape[0], arrGradient)
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


def getPointsOnLine(image, arrGradient, padding):
	xArr, _ = utils.getLineBestFit(image.shape[0], arrGradient)
	newImage = np.zeros(image.shape, image.dtype)

	for j in range(image.shape[0]):
		for i in range(image.shape[1]):
			
			# i is essentially y-1
			# if i == 180:
				# print(i)
			if ((i > (xArr[1][j] + padding)) and (i < xArr[3][j] + (padding+1))):
				newImage[j][i] = image[j][i]	

			# if (x > (lineArr[1][i] + padding) and x < (xArr[y][x] - padding)):

			# if (x > xArr[2][x] and x < xArr[3][x]):
			# 	newImage[y][x] = image[y][x]		
	return newImage

def withinBounds(x, y):
		if (x > 300 and y > 200) and (x < 550 and y < 800):
			return True
		else:
			return False 

def getX(y, m, c):
		return (y-c) / m

def calcSecondDeriv(image):
	# betterSecondDeriv
	# take the lowest y and x coord that sits on the green and red line

	# use equation of green and red line to find x coord at lowest and max height
	# set value of points outside these bounds to zero

# 
	# secDerivExtract = np.zeros(image.shape)

	# for i in range(len(image)):
	# 	for j in range(len(image[0])):
	# 		if withinBounds(j, i):
	# 			secDerivExtract[i][j] = image[i][j]

	gradientArr, _ = lineOfBestFit(image)
	secDerivExtract = getPointsOnLine(image, gradientArr, padding=20)


	return secDerivExtract


# def getLineBestFit(yRange, arrGradient, arrLines):
# 	m = 0
# 	c = 0
# 	xArr = []
# 	yArr = []
	

# 	for i in range(yRange):
# 		yArr.append(i)

# 	for j in range(len(arrGradient)):
# 		m,c = arrGradient[j]
# 		xArr.append([])
# 		for i in range(yRange):
# 			xArr[j].append((i - c)/m)

# 	return (xArr, yArr)
