import pygame, sys, time
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

		self.x = posX
		self.y = posY
		self.width = width
		self.height = height
		self.keys = keys

		self.velocity = vector(0, 0)
		self.accel = vector(0, 0)
		self.acceleration = 50000
		self.maxSpeed = 5
		self.jumpStren = 1

		self.time = 0
		self.lastAccel = 0

		self.oldRect = None
		self.isJumping = False
		self.jumpStart = 0
		self.isMoving = False
		self.movingDirection = ''

	def update(self):
		self.move()
		self.updateVars()

		self.time = time.time()

		self.show()

	def updateVars(self):
		self.x += self.velocity.x
		self.y += self.velocity.y

	def show(self):
		print 'V: ',self.velocity.vector()
		print 'A: ',self.accel.vector()
		print

	def move(self):
		self.handleVelocity()
		newpos = self.rect.move((self.velocity.x, self.velocity.y))
		if self.isFree(newpos):
			self.oldRect = self.rect
			self.rect = newpos

	def handleVelocity(self):
		dt = self.time - self.lastAccel

		self.velocity = self.velocity + self.accel * dt

		if self.velocity.x > self.maxSpeed:
			self.velocity.setX(self.maxSpeed)
		elif self.velocity.x < -self.maxSpeed:
			self.velocity.setX(-self.maxSpeed)

		self.lastAccel = time.time()

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

		if button == self.keys['UP'] and not self.isJumping:
			self.jump()

	def accelerate(self):
		if self.movingDirection == "RIGHT":
			self.accel.changeX(self.acceleration)
		elif self.movingDirection == "LEFT":
			self.accel.changeX(-self.acceleration)

	def jump(self):
		print "Jump"

	def isFree(self, pos):
		return True

	def collide(self, withWhat):
		collision = self.rect.collidelistall(withWhat)
		if collision:
			self.isMoving = False
			self.rect = self.oldRect
		if self.rect.collidelistall(withWhat):
			self.jump()


class keySet(object):
	def __init__(self):
		self.sets = []

		self.sets.append({'UP':119, 'RIGHT':100, 'LEFT':97}) # wasd
		self.sets.append({'UP':273, 'RIGHT':275, 'LEFT':276})# arrows

	def getSet(self, num):
		return self.sets[num]



