import pygame
from pygame.locals import *

class player(pygame.sprite.Sprite):
	'''
	Class to handle several players
	'''
	def __init__(self, posX, posY, path2pic, width, height):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()

		self.image, self.rect = i.load_image(path2pic, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY

		self.x = posX
		self.y = posY
		self.width = width
		self.height = height

		self.speed = 4
		self.jump = 30

		self.isJumping = False
		self.isMoving = False

	def update(self):
		if self.isMoving:
			self._move(self.speed)

	def _move(self, hori = 0, verti = 0):
		newpos = self.rect.move((hori, verti))
		if not self.area.contains(newpos):
			print "Moved outside of the screen..."
		self.rect = newpos

	def steer(self, button, move):
		if move:
			if button == 97: # a
				self.isMoving = True
				if self.speed > 0:
					self.speed = -self.speed
			elif button == 100: # d
				self.isMoving = True
				if self.speed < 0:
					self.speed = -self.speed
		else:
			self.isMoving = False

		if button == 119 and not self.isJumping: # w
			self.isJumping = True
			self._move(0, -self.jump)


class world(object):
	'''
	Class to react to the environment
	'''
	def __init__(self, width, height):
		self.gravity = 9.81

		self.width = width
		self.height = height
		
		self.objList = []

	def addObject(self, obj):
		self.objList.append(obj)

	def update(self):
		for o in self.objList:
			o.update()
			if o.rect.bottom < self.height:
					o._move(0, 1)
					if o.rect.bottom >= self.height:
						o.isJumping = False
				


class handleImg(object):
	'''
	Class to handle the graphical part
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




