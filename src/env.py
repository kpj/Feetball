import sprites, os, useful, random
from var import *

class world(object):
	'''
	Class to react to the environment
	'''
	def __init__(self, width, height):
		self.gravity = GRAVITY
		self.frictionGround = FRICTIONG
		self.frictionAir = FRICTIONA

		self.width = width
		self.height = height

		self.objList = []
		self.arcs = []
		self.rects = []

	def addObject(self, obj):
		self.objList.append(obj)
		try:
			obj.r # only circles have got a radius
			self.arcs.append(obj)
		except AttributeError:
			self.rects.append(obj)

	def spawnBall(self):
		for o in self.arcs:
			if not o.what:
				o.rect.centerx = BALLSTARTX
				o.rect.centery = BALLSTARTY
				o.accel.makeZero()
				o.velocity.makeZero()
				x = random.uniform(float(-BALLSTARTV), float(BALLSTARTV))
				y = random.uniform(float(-BALLSTARTV), -1)
				o.velocity.setX(x)
				o.velocity.setY(y)

	def getObjects(self):
		return self.objList

	def getArcs(self):
		return self.arcs

	def getRects(self):
		return self.rects

	def makeStuff(self):
		self.update()
		self.handleFriction()
		self.handleGravity()

	def update(self):
		for o in self.objList:
			o.tellCurrentObjects(self.arcs, self.rects)
			o.update()
			try:
				if o.newBall:
					# Need new ball
					o.setBallState(False)
					self.spawnBall()
			except AttributeError:
				pass

	def handleFriction(self):
		try:
			for o in self.objList:
				if not o.isMoving:
					if o.inAir:
#						o.velocity.setX(o.velocity.x * self.frictionAir * (float(9)/o.m))
						o.velocity.setX(o.velocity.x * self.frictionAir)
					else:
						o.velocity.setX(o.velocity.x * self.frictionGround * (float(7)/o.m))
					o.accel.setX(0)
		except AttributeError:
			pass

	def handleGravity(self):
		for o in self.arcs:
			o.velocity.changeY(self.gravity * o.m)

	def steer(self, k, b):
		for o in self.objList:
			o.steer(k, b)
