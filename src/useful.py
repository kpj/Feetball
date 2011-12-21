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

	def length(self):
		return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


class handleImg(object):
	'''
	Class to handle images
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
		return image, image.get_rect()
