import pygame, sys, time, math
from pygame.locals import *
from useful import *

class player(pygame.sprite.Sprite):
	'''
	Class to handle several players
	'''
	def __init__(self, posX, posY, path2pic, keys):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()

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
		self.m = 10

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
		self.position = self.position + self.velocity

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

		self.velocity = self.velocity + self.accel  * dt

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
		try:
			myPos = vector(self.rect.centerx, self.rect.centery)
			for o in withWhat:
				hisPos = vector(o.rect.centerx, o.rect.centery)
				diff = hisPos - myPos
				dist = diff.length()
				minDist = self.r + o.r
				if dist < minDist:
					angle = math.atan2(diff.y, diff.x)
					sine = math.sin(angle)
					cose = math.cos(angle)

					tmp1 = vector(0,0)
					tmp2 = vector(cose * diff.x + sine * diff.y, cose * diff.x - sine * diff.y)

					myV = vector(cose * self.velocity.x + sine * self.velocity.y, cose * self.velocity.x - sine * self.velocity.y)
					hisV = vector(cose * o.velocity.x + sine * o.velocity.y, cose * o.velocity.x - sine * o.velocity.y)

					myfV = vector(0,0)
					myfV.setX(((self.m-o.m) * myV.x + 2 * o.m * hisV.x) / (self.m + o.m), )
					myfV.setY(myV.y)

					hisfV = vector(0,0)
					hisfV.setX(((o.m-self.m) * hisV.x + 2 * self.m * myV.x) / (self.m + o.m), )
					hisfV.setY(hisV.y)

					tmp1.changeX(myfV.x)
					tmp2.changeX(hisfV.x)

					f1 = vector(cose * tmp1.x - sine * tmp1.y, cose * tmp1.y + sine * tmp1.x)
					f2 = vector(cose * tmp2.x - sine * tmp2.y, cose * tmp2.y + sine * tmp2.x)

					self.velocity.setX(cose * f1.x - sine * f1.y)
					self.velocity.setY(cose * f1.y + sine * f1.x)
					o.velocity.setX(cose * f2.x - sine * f2.y)
					self.velocity.setY(cose * f2.y + sine * f2.x)

#					targetX = myPos.x + cose * minDist
#					targetY = myPos.y + sine * minDist

#					ax = (targetX - hisPos.x) * 0.05
#					ay = (targetY - hisPos.y) * 0.05

#					print ax,ay
#					self.velocity.changeY(-ax)
#					self.velocity.changeY(-ay)

#					o.velocity.changeX(-ax)
#					o.velocity.changeY(-ay)

		except AttributeError:
			pass
			

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


