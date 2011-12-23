import pygame, sys, time, math
from pygame.locals import *
from useful import *

class sphere(pygame.sprite.Sprite):
	'''
	Class to handle several players
	'''
	def __init__(self, posX, posY, path2pic, keys, m, what):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()
		self.c = collisions()

		self.image, self.rect, self.surface = i.load_image(path2pic, -1)
		self.screen = pygame.display.get_surface()
		self.area = self.screen.get_rect()
		self.rect.topleft = posX, posY

		self.x = posX
		self.y = posY
		self.width = self.surface[0]
		self.height = self.surface[1]
		self.keys = keys
		self.position = vector(self.x, self.y)

		self.r = self.height/2
		self.m = m
		self.what = what # True -> player ; False -> ball

		self.velocity = vector(0, 0)
		self.accel = vector(0, 0)
		self.acceleration = 50000
		self.maxSpeedX = 5
		self.maxSpeedY = 15
		self.jumpStren = 6

		self.time = 0
		self.lastAccel = 0

		self.oldRect = None
		self.isJumping = False
		self.jumpStart = 0
		self.isMoving = False
		self.inAir = False
		self.movingDirection = ''

		self.arcs = []
		self.rects = []

	def update(self):
		self.move()
		self.updateVars()

		self.time = time.time()

#		self.show()

	def tellCurrentObjects(self, arcs, rects):
		self.arcs = arcs
		self.rects = rects	

	def updateVars(self):
		self.position.setX(self.rect.centerx)
		self.position.setY(self.rect.centery)

	def show(self):
		print 'V: ',self.velocity.vector()
		print 'A: ',self.accel.vector()
		print

	def move(self):
		self.handleVelocity()

		newpos = self.rectCollide()

		self.arcCollide()

		self.oldRect = self.rect
		self.rect = newpos

	def handleVelocity(self):
		dt = self.time - self.lastAccel

		self.velocity = self.velocity + self.accel  * dt

		if self.velocity.x > self.maxSpeedX:
			self.velocity.setX(self.maxSpeedX)
		elif self.velocity.x < -self.maxSpeedX:
			self.velocity.setX(-self.maxSpeedX)

		if self.velocity.y > self.maxSpeedY:
			self.velocity.setY(self.maxSpeedY)
		elif self.velocity.y < -self.maxSpeedY:
			self.velocity.setY(-self.maxSpeedY)

		self.lastAccel = time.time()

	def steer(self, button, move):
		if not self.what:
			return 

		if (button == self.keys['LEFT'] or button == self.keys['RIGHT']):
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
			self.isJumping = True
			self.jump()

	def accelerate(self):
		if self.movingDirection == "RIGHT":
			self.accel.changeX(self.acceleration)
		elif self.movingDirection == "LEFT":
			self.accel.changeX(-self.acceleration)

	def jump(self):
		self.velocity.setY(-self.jumpStren)

	def arcCollide(self):
		for o in self.arcs:
			scal = (o.position - self.position) * self.velocity

			dist = (self.position - o.position).length()
			if dist <= self.r + o.r and dist != 0 and scal > 0:
				pulse1 = self.velocity * self.m
				pulse2 = o.velocity * o.m

				self.velocity = pulse2 * (float(1) / self.m)
				o.velocity = pulse1 * (float(1) / o.m)

	def rectCollide(self):
		tmp = self.rect.copy()
		xCol = self.rectCollideX(tmp)
		yCol = self.rectCollideY(tmp)

		if yCol:
			# Touched some ground
			self.isJumping = False
			self.inAir = False
		else:
			self.inAir = True

		if not xCol and not yCol:
			newpos = self.rect.move((self.velocity.x, self.velocity.y))
		elif not xCol and yCol:
			newpos = self.rect.move((self.velocity.x, 0))
		elif not yCol and xCol:
			newpos = self.rect.move((0, self.velocity.y))
		else:
			newpos = self.rect

		return newpos

	def rectCollideX(self, pos):
		for o in self.rects:
			xMove = pos.move((self.velocity.x, 0))
			colX = self.c.rectCollide(xMove, o)
			if colX:
				return True
		return False
			
	def rectCollideY(self, pos):
		for o in self.rects:
			yMove = pos.move((0, self.velocity.y))
			colY = self.c.rectCollide(yMove, o)
			if colY:
				return True
		return False


class wall(pygame.sprite.Sprite):
	def __init__(self, posX, posY, path2pic):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()

		self.image, self.rect, self.surface = i.load_image(path2pic, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY

		self.x = posX
		self.y = posY
		self.width = self.surface[0]
		self.height = self.surface[1]
		self.position = vector(self.x-self.width/2, self.y-self.height/2)

	def steer(self, rofl, xD):
		pass

	def update(self):
		pass

	def collide(self, withWhat):
		pass

	def tellCurrentObjects(self, arcs, rects):
		pass
