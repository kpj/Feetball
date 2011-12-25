import pygame, math, time
from pygame.locals import *

class vector(object):
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

	def changeX(self, x):
		self.x += x

	def changeY(self, y):
		self.y += y

	def makeZero(self):
		self.x = 0
		self.y = 0

	def vector(self):
		return '[%f, %f]' % (self.x, self.y)

	def __add__(self, vec):
		return vector(self.x + vec.x, self.y + vec.y)

	def __sub__(self, vec):
		return vector(self.x - vec.x, self.y - vec.y)

	def __mul__(self, var):
		if type(var) == type(int(1)) or type(var) == type(float(1)):
			return vector(self.x * var, self.y * var)
		elif type(var) == type(vector(1,1)):
			return self.x * var.x + self.y * var.y

	def __div__(self, var):
		if type(var) == type(int(1)) or type(var) == type(float(1)):
			return vector(self.x / var, self.y / var)
		elif type(var) == type(vector(1,1)):
			return -1

	def length(self):
		return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


class mathy(object):
	def getClosestPointToLine(self, start, end, point):
		A1 = end.y - start.y
		B1 = start.x - end.x

		C1 = A1 * start.x + B1 * start.y
		C2 = -B1 * point.x + A1 * point.y

		det = A1*A1 - -B1*B1
		c = vector(0, 0)

		if det != 0:
			c.setX(float( ( A1 * C1 - B1 * C2 ) / det ))
			c.setY(float( ( A1 * C2 - -B1 * C1) / det ))
		else:
			c.setX(point.x)
			c.setY(point.y)

		return c


class collisions(mathy):
	def __init__(self):
		pass

	def circleCollide(self, c1, c2):
		'''
		Return False, if no collision is detected
		Return collision-free points, if collision is detected
		'''
		dist = (c1.position - c2.position).length()
		if dist <= c1.r + c2.r and dist != 0:
			middle = vector( (c1.x + c2.x) / 2, (c1.y + c2.y) / 2)
			new1 = vector(middle.x + c1.r * (c1.position.x - c2.position.x) / dist, middle.y + c1.r * (c1.position.y - c2.position.y) / dist)
			new2 = vector(middle.x + c2.r * (c2.position.x - c1.position.x) / dist, middle.y + c2.r * (c2.position.y - c1.position.y) / dist)
			return new1, new2
		else:
			return False

	def rectCollide(self, r1, r2):
		if	r1.colliderect(r2):
			return True
		else:
			return False


class keySet(object):
	def __init__(self):
		self.sets = []

		self.sets.append({'UP':119, 'RIGHT':100, 'LEFT':97, 'SHOOT':32}) # wasd + space
		self.sets.append({'UP':273, 'RIGHT':275, 'LEFT':276, 'SHOOT':112})# arrows + p

	def getSet(self, num):
		return self.sets[num]


class handleImg(object):
	'''
	Class to handle extern data
	'''
	def load_image(self, path, colorkey=None):
		try:
			image = pygame.image.load(path)
		except pygame.error, message:
			print 'Cannot load image:', path
			raise SystemExit, message
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
				image.set_colorkey(colorkey, RLEACCEL)
		return image, image.get_rect(), image.get_rect().bottomright

	def load_sound(self, path):
		class NoneSound:
			def play(self): pass
		if not pygame.mixer:
			return NoneSound()
		try:
			sound = pygame.mixer.Sound(path)
		except pygame.error, message:
			print 'Cannot load sound:', path
			raise SystemExit, message
		return sound
