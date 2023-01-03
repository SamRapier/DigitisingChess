import cv2, numpy as np
import math
import debug

def slid_detector(img, alfa=150, beta=2):
	"""detect lines using Hough algorithm"""
	__lines, lines = [], cv2.HoughLinesP(img, rho=1, theta=np.pi/360*beta,
		threshold=40, minLineLength=50, maxLineGap=15) # [40, 40, 10]

	if lines is None: 
		return []

	for line in np.reshape(lines, (-1, 4)):
		__lines += [[[int(line[0]), int(line[1])],
					 [int(line[2]), int(line[3])]]]

	return __lines

def SLID(img, segments):
	# FIXME: zrobic 2 rodzaje haszowania (katy + pasy [blad - delta])
	# print(utils.call("SLID(img, segments)"))
	
	global all_points; all_points = []
	pregroup, group, hashmap, raw_lines = [[], []], {}, {}, []

	__cache = {}
	def __dis(a, b):
		"""
		Get the distance between two lines and stores in in cache using a hash of the two inputs
		"""
		idx = hash("__dis" + str(a) + str(b))
		if idx in __cache: return __cache[idx]
		# get the matrix normalised value for point a - point b
		__cache[idx] = np.linalg.norm(np.array(a)-np.array(b))
		return __cache[idx]

	X = {}
	def __fi(x):
		"""
		
		"""
		if x not in X: X[x] = 0

		if (X[x] == x or X[x] == 0):
			X[x] = x
		else:
			X[x] = __fi(X[x])

		return X[x]

	def __un(a, b):
		"""
		Get the union of two hashes
		"""
		ia, ib = __fi(a), __fi(b)
		X[ia] = ib
		group[ib] |= group[ia]
		#group[ia] = set()
		#group[ia] = set()

	# shortest path // height
	# returns a matrix norm of the cross-product of the inputs to calculate the shortest path between the points
	nln = lambda l1, x, dx: \
		np.linalg.norm(np.cross(np.array(l1[1])-np.array(l1[0]),
								np.array(l1[0])-np.array(   x)))/dx

	def __similar(line_1, line_2):
		"""
		check to see if two lines are similar
		"""
		dist_a = __dis(line_1[0], line_1[1])
		dist_b = __dis(line_2[0], line_2[1])
		# if da > db: l1, l2, da, db = l2, l1, db, da

		dist_1a = nln(line_1, line_2[0], dist_a)
		dist_2a = nln(line_1, line_2[1], dist_a)

		dist_1b = nln(line_2, line_1[0], dist_b) 
		dist_2b = nln(line_2, line_1[1], dist_b)
	
		dist_sum = 0.25 * (dist_1a + dist_1b + dist_2a + dist_2b) + 0.00001
		#print(da, db, abs(da-db))
		#print(int(da/ds), int(db/ds), "|", int(abs(da-db)), int(da+db),
		#		int(da+db)/(int(abs(da-db))+0.00001))
		alfa = 0.0625 * (dist_a + dist_b) #15
		# FIXME: roznica???
		#if d1 + d2 == 0: d1 += 0.00001 # [FIXME]: divide by 0
		t1 = (dist_a/dist_sum > alfa and dist_b/dist_sum > alfa)
		if not t1: 
			return False # [FIXME]: dist???
		
		return True

	def __generate(a, b, num):
		points = []; t = 1/num
		for i in range(num):
			x = a[0] + (b[0]-a[0]) * (i * t)
			y = a[1] + (b[1]-a[1]) * (i * t)
			points += [[int(x), int(y)]]
		return points

	def __analyze(group):
		global all_points
		points = []
		for idx in group:
			points += __generate(*hashmap[idx], 10)
		_, radius = cv2.minEnclosingCircle(np.array(points))
		w = radius * (math.pi/2)
		diameter = 2*radius
		# (cx, cy) are points on the line
		# (vx, vy) is a normalised vector which is collinear to the line that (cx, cy) lies on
		vx, vy, cx, cy = cv2.fitLine(np.array(points), cv2.DIST_L2, 0, 0.01, 0.01)
		debug.color()
		all_points += points

		# rawLine = [[int(cx-vx*w), int(cy-vy*w)], [int(cx+vx*w), int(cy+vy*w)]]
		rawLine = [[int(cx-vx*radius), int(cy-vy*radius)], [int(cx+vx*radius), int(cy+vy*radius)]]
		return rawLine

	# hashes each segment and saves them in a hashmap
	# not sure exactly why we have group and X as well as hashmap
	# works out if there is a vertical or horizontal line
	# pregroup[0] holds vertical? lines
	# pregroup[1] holds horizontal? lines
	for l in segments:
		h = hash(str(l))
		t1 = l[0][0] - l[1][0]
		t2 = l[0][1] - l[1][1]

		hashmap[h] = l
		group[h] = set([h])
		X[h] = h

		if abs(t1) < abs(t2): 
			pregroup[0].append(l)
		else:                 
			pregroup[1].append(l)

	debug.image(img.shape) \
		.lines(pregroup[0], color=debug.color()) \
		.lines(pregroup[1], color=debug.color()) \
	.save("slid_pre_groups")

	# vertical and horizontal lines
	for lines in pregroup:
		# for each horizontal/vertical line
		for i in range(len(lines)):
			# get the line and its respective hash
			l1 = lines[i]
			h1 = hash(str(l1))

			#print(h1, __fi(h1))
			# check to ensure the hashes match
			if (X[h1] != h1): 
				continue

			#if (__fi(h1) != h1): continue

			# loop through all the lines again and check to see if they are similar so they can be grouped together
			for j in range(i+1, len(lines)):
				l2 = lines[j]
				h2 = hash(str(l2))

				#if (__fi(h2) != h2): continue

				# check to ensure the hashes match
				if (X[h2] != h2): 
					continue
				#if (len(group[h2])==0): continue
				# if not similar, skip to next line
				if not __similar(l1, l2): 
					continue
				# get the union of the two hashes if they are similar
				__un(h1, h2) # union & find

				# break # FIXME

	__d = debug.image(img.shape)
	# for each hash in a group 
	# Sets the line colour in the debug image for each group of lines and then saves the image
	for i in group:
		#if (__fi(i) != i): continue
		# find the root hash
		if (X[i] != i): 
			continue
		#if len(group[i]) == 0: continue
		# 
		ls = [hashmap[h] for h in group[i]]
		__d.lines(ls, color=debug.color())
	__d.save("slid_all_groups")


	for i in group:
		#if (__fi(i) != i): continue
		if (X[i] != i): continue
		#if len(group[i]) == 0: continue
		#if (__fi(i) != i): continue
		raw_lines += [__analyze(group[i])]
	debug.image(img.shape).lines(raw_lines).save("slid_final")

	debug.image(img.shape)\
		.points(all_points, color=(0,255,0), size=2)\
	.lines(raw_lines).save("slid_final2")

	return raw_lines

def slid_tendency(raw_lines, s=4): # FIXME: [1.25 -> 2]
	# print(utils.call("slid_tendency(raw_lines)"))
	lines = []; scale = lambda x, y, s: \
		int(x * (1+s)/2 + y * (1-s)/2)
	for a, b in raw_lines:
		# [A] s - scale
		# Xa' = Xa (1+s)/2 + Xb (1-s)/2
		# Ya' = Ya (1+s)/2 + Yb (1-s)/2
		a[0] = scale(a[0], b[0], s)
		a[1] = scale(a[1], b[1], s)
		# [B] s - scale
		# Xb' = Xb (1+s)/2 + Xa (1-s)/2
		# Yb' = Yb (1+s)/2 + Ya (1-s)/2
		b[0] = scale(b[0], a[0], s)
		b[1] = scale(b[1], a[1], s)
		lines += [[a, b]]
	return lines