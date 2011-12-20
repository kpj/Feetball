import pygame
from pygame.locals import *

class player(pygame.sprite.Sprite):
	'''
	Class to handle several players
	'''
	def __init__(self, posX, posY, path2pic, width, height, keys):
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
		self.keys = keys

		self.speed = 4
		self.jump = 40

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
		if button == self.keys['LEFT'] or button == self.keys['RIGHT']:
			if move:
				if button == self.keys['LEFT']: # a
					self.isMoving = True
					if self.speed > 0:
						self.speed = -self.speed
				elif button == self.keys['RIGHT']: # d
					self.isMoving = True
					if self.speed < 0:
						self.speed = -self.speed
			else:
				self.isMoving = False

		if button == self.keys['UP'] and not self.isJumping: # w
			self.isJumping = True
			self._move(0, -self.jump)


class world(object):
	'''
	Class to react to the environment
	'''
	def __init__(self, width, height):
		self.gravity = 2

		self.width = width
		self.height = height
		
		self.objList = []

	def addObject(self, obj):
		self.objList.append(obj)

	def update(self):
		for o in self.objList:
			o.update()
			if o.rect.bottom < self.height:
					o._move(0, self.gravity)
					if o.rect.bottom >= self.height:
						o.isJumping = False

	def steer(self, k, b):
		for o in self.objList:
			o.steer(k, b)
				

class keySet(object):
	def __init__(self):
		self.sets = []

		self.sets.append({'UP':119, 'RIGHT':100, 'LEFT':97})
		self.sets.append({'UP':273, 'RIGHT':275, 'LEFT':276})

	def getSet(self, num):
		return self.sets[num]


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




