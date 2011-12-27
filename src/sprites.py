import pygame, sys, time, math, os
from pygame.locals import *
from useful import *
from var import *

class sphere(pygame.sprite.Sprite):
	def __init__(self, posX=0, posY=0, path2pic=os.path.join('img', 'ball.png'), keys=None, m=1, what=True, pid=42, name='kpj', bounce=0.6):
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

		self.arcCollide() # 2, 3, 4

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
			minDist = self.r + o.r
			if dist <= minDist and scal > 0:
				pulse1 = self.velocity * self.m
				pulse2 = o.velocity * o.m

				self.velocity = pulse2 * (float(1) / self.m)
				o.velocity = pulse1 * (float(1) / o.m)

				# Won't overlap, but very strange looking + gets stuck in walls
#				overlap = minDist - dist
#				v = o.position - self.position
#				v /= 2
#				self.rect.centerx -= v.x
#				self.rect.centery -= v.y
#				o.rect.centerx += v.x
#				o.rect.centery += v.y

				# Minimal better collision detection, but ends in heavy lagging
#			while dist <= self.r + o.r and dist != 0:
#				self.rect.centerx -= self.velocity.x
#				self.rect.centery -= self.velocity.y
#				self.position -= self.velocity
#				dist = (self.position - o.position).length()

	def arcCollide2(self):
		for o in self.arcs:
			# Get closest point on own movement to the other circle, to determine, if a collision would happen
			d = self.c.getClosestPointToLine(self.position, self.position + self.velocity, o.position)
			closestDistSQR = pow(o.position.x - d.x, 2) + pow(o.position.y - d.y, 2)
			print closestDistSQR, pow(self.r + o.r,2)
			if closestDistSQR <= pow(self.r + o.r,2) and closestDistSQR != 0:
				# Is collision
				# This gives us the point of collision
				backdist = math.sqrt( pow(self.r+o.r,2) - closestDistSQR)
				movementvectorlength = self.velocity.length()
				c_x = d.x - backdist * (self.velocity.x / movementvectorlength)
				c_y = d.y - backdist * (self.velocity.y / movementvectorlength)

				# Calc norm vectors
				collisiondist = math.sqrt(pow(o.position.x - c_x, 2) + pow(o.position.y - c_y, 2))
				n_x = (o.position.x - c_x) / collisiondist
				n_y = (o.position.y - c_y) / collisiondist

				# Calc some other norm vectors
				nx = (o.position.x - self.position.x) / collisiondist
				ny = (o.position.y - self.position.y) / collisiondist

				# Relate everything
				p = 2 * (self.velocity.x * nx + self.velocity.y * n_y - o.velocity.x * nx - o.velocity.y * n_y) / (self.m + o.m)

				self.velocity.setX(self.velocity.x - p * self.m * n_x)
				self.velocity.setY(self.velocity.y - p * self.m * n_y)
				o.velocity.setX(o.velocity.x + p * o.m * n_x)
				o.velocity.setY(o.velocity.y + p * o.m * n_y)
			else:
				# No collision
				pass

	def arcCollide3(self):
		for o in self.arcs:
			dist = self.position - o.position
			if dist.length() <= self.r + o.r:
				# Is collision
				theta = math.atan2(dist.y, dist.x)
				sine = math.sin(theta)
				cosine = math.cos(theta)

				tmpS = [sphere(), sphere()]
				tmpS[1].position.x = cosine * dist.x + sine * dist.y
				tmpS[1].position.y = cosine * dist.y -sine * dist.x

				tmpV = [vector(0,0), vector(0,0)]
				tmpV[0].x = cosine * self.velocity.x + sine * self.velocity.y
				tmpV[0].y = cosine * self.velocity.y - sine * self.velocity.x
				tmpV[1].x = cosine * o.velocity.x + sine * o.velocity.y
				tmpV[1].y = cosine * o.velocity.y - sine * o.velocity.x

				vFinal = [vector(0,0), vector(0,0)]
				vFinal[0].x = ((self.m - o.m) * tmpV[0].x + 2 * o.m * tmpV[1].x) / (self.m + o.m)
				vFinal[0].y = tmpV[0].y
				vFinal[1].x = ((o.m - self.m) * tmpV[1].x + 2 * self.m * tmpV[1].x) / (self.m + o.m)
				vFinal[1].y = tmpV[1].y

				tmpS[0].position.x += vFinal[0].x
				tmpS[1].position.x += vFinal[1].x

				bFinal = [sphere(), sphere()]
				bFinal[0].position.x = cosine * tmpS[0].position.x - sine * tmpS[0].y
				bFinal[0].position.y = cosine * tmpS[0].position.y + sine * tmpS[0].x
				bFinal[1].position.x = cosine * tmpS[1].position.x - sine * tmpS[1].y
				bFinal[1].position.y = cosine * tmpS[1].position.y + sine * tmpS[1].x

				o.position.x += bFinal[1].position.x
				o.position.y += bFinal[1].position.y
				self.position.x += bFinal[0].position.x
				self.position.y += bFinal[0].position.y

				self.velocity.x = cosine * vFinal[0].x - sine * vFinal[0].y
				self.velocity.y = cosine * vFinal[0].y + sine * vFinal[0].x
				o.velocity.x = cosine * vFinal[1].x - sine * vFinal[1].y
				o.velocity.y = cosine * vFinal[1].y + sine * vFinal[1].x

	def arcCollide4(self):
		spring = 1
		for o in self.arcs:
			dx = o.position.x - self.position.x
			dy = o.position.y - self.position.y
			minDist = self.r + o.r
			if (o.position - self.position).length() <= minDist and (o.position - self.position).length() != 0:
				# Is collision
				angle = math.atan2(dy, dx)
				targetX = self.position.x + math.cos(angle) * minDist
				targetY = self.position.y + math.sin(angle) * minDist
				ax = (targetX - o.position.x) * spring
				ay = (targetY - o.position.y) * spring
				self.velocity.x -= ax
				self.velocity.y -= ay
				o.velocity.x += ax
				o.velocity.y += ay

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
		self.wantsParticles = False

#		self.shotsound = i.load_sound(SHOTSOUND)

	def footCollide(self):
		for o in self.arcs:
			if not o.what:
				# Hits ball
				scal = (o.position - self.point) * self.velocity

				dist = (self.point - o.position).length()
				if dist <= self.r + o.r and dist != 0 and scal > 0:
					# Foot touches ball
#					self.shotsound.play()
					# Test sound
					pulse1 = self.velocity * self.m
					pulse2 = o.velocity * o.m

					o.velocity = pulse1 * (float(1) / o.m)

					# Lets create some particles
					self.wantsParticles = True

	def steer(self, rofl, xD):
		pass

	def update(self):
		self.midPoint = vector(self.player.rect.centerx, self.player.rect.centery)
		self.calcDiffer()

		self.velocity = self.point - self.lastPoint
		self.footCollide()

		self.handleFootPosition()

	def calcDiffer(self):
		# Foot shouldnt be exactly on radius
		self.pointOnCircle = vector(self.midPoint.x, self.midPoint.y + self.r + 13)

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


class powerup(pygame.sprite.Sprite):
	def __init__(self, posX, posY, path2pic, affect, amount, duration):
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
		self.position = vector(self.x-self.width/2, self.y-self.height/2)

		self.affect = affect
		self.amount = amount
		self.duration = duration

		self.start = time.time()
		self.taken = False
		self.destruct = False
		self.player = None

		self.arcs = []

	def onCollide(self, o):
		self.player = o
		oldValue = getattr(o, self.affect)
		newValue = oldValue + self.amount
		if newValue >= 0:
			setattr(o, self.affect, newValue)
		else:
			setattr(o, self.affect, 0)
		self.start = time.time()
		self.taken = True

	def updateVars(self):
		self.position.setX(self.rect.centerx)
		self.position.setY(self.rect.centery)

	def steer(self, rofl, xD):
		pass

	def resetPlayer(self):
		if not self.destruct:
			oldValue = getattr(self.player, self.affect)
			setattr(self.player, self.affect, oldValue - self.amount)
			self.destruct = True

	def handleBehavior(self):
		if self.taken:
			# Player touched me
			if time.time() >= self.start + self.duration:
				# My time has come
				self.resetPlayer()
		else:
			# No one touched me
			pass

	def update(self):
		self.handleBehavior()
		self.updateVars()

		self.checkCollisions()

	def checkCollisions(self):
		for o in self.arcs:
			if self.c.rectCollide(self.rect, o.rect) and o.what:
				# Is colliding player
				self.onCollide(o)

	def collide(self, withWhat):
		pass

	def tellCurrentObjects(self, arcs, rects, feet):
		self.arcs = arcs


class particle(pygame.sprite.Sprite):
	def __init__(self, posX, posY, dur, startTime, color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((5, 5)).convert()
		self.rect = self.image.get_rect()
		self.screen = pygame.display.get_surface()
		self.area = self.screen.get_rect()
		self.rect.center = posX, posY

		self.x = posX
		self.y = posY
		self.startTime = startTime
		self.duration = dur
		self.color = color # one color -> (x, y, z) ; blink -> False

		self.destruct = False

		self.vx = random.uniform(-2,2)
		self.vy = random.uniform(-1,-0.2)
		self.ax = random.uniform(-0.2,0.2)
		self.ay = random.uniform(0,0.3)

	def update(self):
		if self.color:
			# Just one color
			self.image.fill(self.color)
		else:
			# Every color
			self.image.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

		self.move()

	def move(self):
		self.rect.centerx += self.vx
		self.rect.centery += self.vy
		self.updateVelocity()
		self.handleTime()

	def handleTime(self):
		if time.time() - self.startTime > self.duration:
			self.destruct = True

	def updateVelocity(self):
		self.vx += self.ax
		self.vy += self.ay

