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

		self.field = self.area.bottom - 50

		self.x = posX
		self.y = posY
		self.width = width
		self.height = height
		self.keys = keys

		self.velocity = vector(0, 0)
		self.accel = vector(0, 0)
		self.maxSpeed = 5
		self.jumpStren = 8
		self.oldRect = None

		self.isJumping = False
		self.isMoving = False

	def update(self):
		self.move()

#		self.show()

	def show(self):
		print 'V: ',self.velocity.vector()
		print 'A: ',self.accel.vector()
		print

	def slow(self):
		if self.velocity < 0:
			self.accel.setX(self.friction)
		elif self.velocity > 0:
			self.accel.setX(-self.friction)
		else:
			print "Should stand now..."

	def handleFriction(self, friction):
		if not self.isMoving:
			#print "stops"
			pass

	def handleGravity(self, gravity):
		if self.rect.bottom >= self.field:
			self.velocity.setY(0)
			self.accel.setY(0)

		if self.rect.bottom < self.field and self.isJumping:
			self.accel.changeY(gravity)
		elif self.rect.bottom >= self.field:
			self.isJumping = False

	def move(self):
		self.handleVelocity()
		newpos = self.rect.move((self.velocity.x, self.velocity.y))
		self.oldRect = self.rect
		self.rect = newpos

	def handleVelocity(self):
		self.velocity.addVector(self.accel)

	def steer(self, button, move):
		if button == self.keys['LEFT'] or button == self.keys['RIGHT']:
			if move: 
				# keydown
				if button == self.keys['LEFT']:
					self.isMoving = True
					self.accelerate('LEFT')
				elif button == self.keys['RIGHT']:
					self.isMoving = True
					self.accelerate('RIGHT')
			else: 
				# keyup
				self.isMoving = False

		if button == self.keys['UP'] and not self.isJumping:
			self.jump()

	def accelerate(self, where):
		if where == "RIGHT":
			self.accel.changeX(0.2)
		elif where == "LEFT":
			self.accel.changeX(-0.2)

	def jump(self):
		self.isJumping = True
		self.accel.changeY(-self.jumpStren)

	def collide(self, withWhat):
		collision = self.rect.collidelistall(withWhat)
		if collision:
			self.isMoving = False
			self.rect = self.oldRect
		if self.rect.collidelistall(withWhat):
			self.jump()


class world(object):
	'''
	Class to react to the environment
	'''
	def __init__(self, width, height):
		self.gravity = 2
		self.friction = 0.1

		self.width = width
		self.height = height
		
		self.objList = []

	def addObject(self, obj):
		self.objList.append(obj)

	def getObjects(self):
		return self.objList

	def update(self):
		for o in self.objList:
			o.update()
			o.handleFriction(self.friction)
			o.handleGravity(self.gravity)

	def steer(self, k, b):
		for o in self.objList:
			o.steer(k, b)
				
	def checkCollision(self):
		tmp = []
		for o in self.objList:
			tmp = self.objList[:]
			tmp.remove(o)
			o.collide(tmp)


class keySet(object):
	def __init__(self):
		self.sets = []

		self.sets.append({'UP':119, 'RIGHT':100, 'LEFT':97}) # wasd
		self.sets.append({'UP':273, 'RIGHT':275, 'LEFT':276})# arrows

	def getSet(self, num):
		return self.sets[num]


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

	def addVector(self, vec):
		self.x = self.x + vec.x
		self.y = self.y + vec.y


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




