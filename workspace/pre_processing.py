import cv2
import numpy as np
import math
import functools
from copy import copy



def loadImg(filename):
	"""Load image into memory"""
	return cv2.imread(filename)

def grayScale(image):
	"""Apply gray scaling to image"""
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blurImage(image):
	"""Add Gaussian Blur to image"""
	return cv2.GaussianBlur(image, (3,3), 0)

def image_resize(img, height=500):
	"""resize image to same normalized area (height**2)"""
	pixels = height * height; shape = list(np.shape(img))
	scale = math.sqrt(float(pixels)/float(shape[0]*shape[1]))
	shape[0] *= scale; shape[1] *= scale
	img = cv2.resize(img, (int(shape[1]), int(shape[0])))
	img_shape = np.shape(img)
	return img

def image_scale(pts, scale):
	"""scale to original image size"""
	def __loop(x, y): return [x[0] * y, x[1] * y]
	return list(map(functools.partial(__loop, y=1/scale), pts))

def image_transform(img, points, square_length=150):
	"""crop original image using perspective warp"""
	board_length = square_length * 8
	def __dis(a, b): return np.linalg.norm(np.array(a)-np.array(b))
	def __shi(seq, n=0): return seq[-(n % len(seq)):] + seq[:-(n % len(seq))]
	best_idx, best_val = 0, 10**6
	for idx, val in enumerate(points):
		val = __dis(val, [0, 0])
		if val < best_val:
			best_idx, best_val = idx, val
	pts1 = np.float32(__shi(points, 4 - best_idx))
	pts2 = np.float32([[0, 0], [board_length, 0], \
			[board_length, board_length], [0, board_length]])
	M = cv2.getPerspectiveTransform(pts1, pts2)
	W = cv2.warpPerspective(img, M, (board_length, board_length))
	return W


class ImageObject(object):
	images = {}; scale = 1; shape = (0, 0)

	def __init__(self, filename):
		"""save and prepare image array"""
		self.images['orig'] = loadImg(filename)
		self.images['main'], self.shape, self.scale = \
			blurImage(grayScale(image_resize(self.images['orig']))) # downscale for speed
		# self.images['main'] = blurImage(grayScale(self.images['main']))
		self.images['test'] = copy(self.images['main'])

	def crop(self, pts):
		"""crop using 4 points transform"""
		pts_orig = image_scale(pts, self.scale)
		img_crop = image_transform(self.images['orig'], pts_orig)
		self.__init__(img_crop)