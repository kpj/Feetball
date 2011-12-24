import pygame, sys, time, math
from pygame.locals import *
from useful import *
from var import *

class sphere(pygame.sprite.Sprite):
	'''
	Class to handle several players
	'''
	def __init__(self, posX, posY, path2pic, keys, m, what, pid, name, bounce):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()
		self.c = collisions()

		self.imageBase, self.rect, self.surface = i.load_image(path2pic, -1)
		self.screen = pygame.display.get_surface()
		self.area = self.screen.get_rect()
		self.rect.topleft = posX, posY

		self.x = posX
		self.y = posY
		self.width = self.surface[0]
		self.height = self.surface[1]
		self.keys = keys
		self.position = vector(self.x, self.y)
		self.goalCounter = 0

		self.r = self.height/2
		self.m = m
		self.what = what # True -> player ; False -> ball
		self.pid = pid
		self.name = name
		self.bounce = bounce

		self.velocity = vector(0, 0)
		self.accel = vector(0, 0)
		if self.what:
			self.acceleration = PLAYERACCEL
			self.maxSpeedX = PLAYERMAXSPEEDX
			self.maxSpeedY = PLAYERMAXSPEEDY
			self.jumpStren = PLAYERJUMPSTREN
		else:
			self.acceleration = BALLACCEL
			self.maxSpeedX = BALLMAXSPEEDX
			self.maxSpeedY = BALLMAXSPEEDY
			self.jumpStren = 42

		self.time = 0
		self.lastAccel = 0

		self.oldRect = None
		self.isJumping = False
		self.jumpStart = 0
		self.isMoving = False
		self.inAir = False
		self.isShooting = False
		self.movingDirection = ''
		self.newBall = False
		self.degree = 0

		self.arcs = []
		self.rects = []
		self.feet = []

	def update(self):
		self.move()
		self.updateVars()

		self.time = time.time()

		self.handleShooting()
		self.handleBallRotation()

#		self.show()

	def turn(self, amount):
		oldCenter = self.rect.center
		self.degree += amount
		self.degree %= 360
		self.image = pygame.transform.rotate(self.imageBase, self.degree)

		# Better looking, but worse collision...
#		self.rect = self.image.get_rect()
#		self.rect.center = oldCenter

	def handleBallRotation(self):
		if not self.what:
			# Is ball
			if self.velocity.x <= 0:
				self.turn(self.velocity.length())
			else:
				self.turn(- self.velocity.length())
		else:
			# Is player
			self.image = self.imageBase

	def tellCurrentObjects(self, arcs, rects, feet):
		self.arcs = arcs
		self.rects = rects
		self.feet = feet

	def setBallState(self, w):
		self.newBall = w

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

	def handleShooting(self):
		if self.isShooting:
			if self.pid == P1ID:
				# Is p1
				self.moveFoot(FOOTSPEED)
			else:
				# Is p2
				self.moveFoot(-FOOTSPEED)
		else:
			if self.pid == P1ID:
				# Is p1
				self.moveFoot(-FOOTSPEED)
			else:
				# Is p2
				self.moveFoot(FOOTSPEED)

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
			# Is ball
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

		if button == self.keys["SHOOT"] and move:
			# keydown
			self.isShooting = True
		elif button == self.keys["SHOOT"] and not move:
			# keyup
			self.isShooting = False

	def accelerate(self):
		if self.movingDirection == "RIGHT":
			self.accel.changeX(self.acceleration)
		elif self.movingDirection == "LEFT":
			self.accel.changeX(-self.acceleration)

	def moveFoot(self, val):
		for o in self.feet:
			if o.pid == self.pid:
				# Is my foot
				o.hit(val)

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

			while dist <= self.r + o.r and dist != 0:
				self.rect.centerx -= self.velocity.x
				self.rect.centery -= self.velocity.y
				self.position -= self.velocity
				dist = (self.position - o.position).length()

	def calcRectBounceVelo(self, v):
		change = - self.bounce * v * 0.5
		return change

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

		if not xCol and not yCol: # no collision
			newpos = self.rect.move((self.velocity.x, self.velocity.y))
		elif not xCol and yCol: # collision in Y
			newpos = self.rect.move((self.velocity.x, 0))
			# Bounce
			self.velocity.setY(self.calcRectBounceVelo(self.velocity.y))
		elif not yCol and xCol: # collision in X
			newpos = self.rect.move((0, self.velocity.y))
			# Bounce
			self.velocity.setX(self.calcRectBounceVelo(self.velocity.x))
		else: # collisions everywhere
			newpos = self.rect
			# Bounce
			self.velocity.setX(self.calcRectBounceVelo(self.velocity.x))
			self.velocity.setY(self.calcRectBounceVelo(self.velocity.y))

		return newpos

	def rectCollideX(self, pos):
		for o in self.rects:
			xMove = pos.move((self.velocity.x, 0))
			colX = self.c.rectCollide(xMove, o)
			if colX:
				if o.onCollide(self):
					return True
		return False
			
	def rectCollideY(self, pos):
		for o in self.rects:
			yMove = pos.move((0, self.velocity.y))
			colY = self.c.rectCollide(yMove, o)
			if colY:
				if o.onCollide(self):
					return True
		return False

	def scoreGoal(self):
		self.goalCounter += 1


class foot(pygame.sprite.Sprite):
	def __init__(self, pid, path2pic):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()

		self.image, self.rect, self.surface = i.load_image(path2pic, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()

		self.width = self.surface[0]
		self.height = self.surface[1]

		self.pid = pid

		self.degree = math.pi
		self.point = vector(0, 0)
		self.lastPoint = vector(0, 0)
		self.midPoint = vector(100, 100)
		self.velocity = vector(0, 0)

		self.player = None
		self.r = self.rect.width / 2
		self.m = FOOTMASS

	def arcCollide(self):
		for o in self.arcs:
			if not o.what:
				# Hits ball
				scal = (o.position - self.point) * self.velocity

				dist = (self.point - o.position).length()
				if dist <= self.r + o.r and dist != 0 and scal > 0:
					pulse1 = self.velocity * self.m
					pulse2 = o.velocity * o.m

					o.velocity = pulse1 * (float(1) / o.m)

	def steer(self, rofl, xD):
		pass

	def update(self):
		self.midPoint = vector(self.player.rect.centerx, self.player.rect.centery)
		self.calcDiffer()

		self.velocity = self.point - self.lastPoint
		self.arcCollide()

		self.handleFootPosition()

	def calcDiffer(self):
		self.pointOnCircle = vector(self.midPoint.x, self.midPoint.y + self.r)

		# Very long, but working point calculation
		xCo = (self.pointOnCircle.x - self.midPoint.x) * math.cos(self.degree) - (self.pointOnCircle.y - self.midPoint.y) * math.sin(self.degree) + self.midPoint.x
		yCo = (self.pointOnCircle.x - self.midPoint.x) * math.sin(self.degree) - (self.pointOnCircle.y - self.midPoint.y) * math.cos(self.degree) + self.midPoint.y

		self.lastPoint = self.point
		self.point = vector(xCo, yCo)

	def handleFootPosition(self):
		self.rect.centerx = self.point.x
		self.rect.centery = self.point.y

	def hit(self, amount):
		if self.pid == P1ID:
			# Is p1
			if amount > 0:
				if self.degree < 3.0/2 * math.pi:
					self.degree += amount
			else:
				if self.degree > math.pi:
					self.degree += amount
		elif self.pid == P2ID:
			# Is p2
			if amount > 0:
				if self.degree < math.pi:
					self.degree += amount
			else:
				if self.degree > math.pi / 2:
					self.degree += amount

	def collide(self, withWhat):
		pass

	def tellCurrentObjects(self, arcs, rects, feet):
		self.arcs = arcs
		for o in self.arcs:
			if o.what and o.pid == self.pid:
				# Is player with same id
				self.player = o
				self.r = o.rect.width/2


class wall(pygame.sprite.Sprite):
	def __init__(self, posX, posY, path2pic, what, pid):
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

		self.what = what # True -> Wall ; False -> Goal
		self.pid = pid

		self.arcs = []

	def steer(self, rofl, xD):
		pass

	def update(self):
		pass

	def collide(self, withWhat):
		pass

	def tellCurrentObjects(self, arcs, rects, feet):
		self.arcs = arcs

	def onCollide(self, o):
		if self.what:
			# Is a wall
			return True
		if o.what:
			# Is a player
			return False
		# Is a ball

		for o in self.arcs:
			if self.pid == o.pid:
				o.scoreGoal()

		o.setBallState(True)
		return False
