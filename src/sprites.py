import pygame, sys
from pygame.locals import *
from useful import *

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
		self.acceleration = 0.5
		self.maxSpeed = 5
		self.jumpStren = 8

		self.oldRect = None
		self.isJumping = False
		self.isMoving = False
		self.isSlowing = False
		self.movingDirection = ''

	def update(self):
		self.move()

#		self.show()

	def show(self):
		print 'V: ',self.velocity.vector()
		print 'A: ',self.accel.vector()
		print

	def move(self):
		self.handleVelocity()
		newpos = self.rect.move((self.velocity.x, self.velocity.y))
		self.oldRect = self.rect
		self.rect = newpos

	def handleVelocity(self):
		if abs(self.velocity.x) <= self.maxSpeed:
			self.velocity = self.velocity + self.accel

	def steer(self, button, move):
		if button == self.keys['LEFT'] or button == self.keys['RIGHT']:
			if move: 
				# keydown
				if button == self.keys['LEFT']:
					self.isMoving = True
					self.movingDirection = 'LEFT'
				elif button == self.keys['RIGHT']:
					self.isMoving = True
					self.movingDirection = 'RIGHT'
				self.accelerate()
			else: 
				# keyup
				self.isMoving = False
				self.isSlowing = True

		if button == self.keys['UP'] and not self.isJumping:
			self.jump()

	def accelerate(self):
		if self.movingDirection == "RIGHT":
			self.accel.changeX(self.acceleration)
		elif self.movingDirection == "LEFT":
			self.accel.changeX(-self.acceleration)

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

	def makeStuff(self):
		self.update()
		self.handleGravity()
		self.handleFriction()

	def update(self):
		for o in self.objList:
			o.update()

	def handleGravity(self):
		for o in self.objList:
			if o.rect.bottom >= o.field:
				o.velocity.setY(0)
				o.accel.setY(0)

			if o.rect.bottom < o.field and o.isJumping:
				o.accel.changeY(self.gravity)
			elif o.rect.bottom >= o.field:
				o.isJumping = False

	def handleFriction(self):
		for o in self.objList:
			if not o.isMoving:
				o.velocity.setX(0)
				o.accel.setX(0)

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



