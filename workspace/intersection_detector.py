import bentley_ottmann

def intersections(lines):
	"""find all intersections"""
	__lines = [[(a[0], a[1]), (b[0], b[1])] for a, b in lines]
	return bentley_ottmann.isect_segments(__lines)