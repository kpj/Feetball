import sprites

class world(object):
	'''
	Class to react to the environment
	'''
	def __init__(self, width, height):
		self.gravity = 9.81
		self.friction = 0.9

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

	def getObjects(self):
		return self.objList

	def getArcs(self):
		return self.arcs

	def getRects(self):
		return self.rects

	def makeStuff(self):
		self.update()
		self.handleFriction()

	def update(self):
		for o in self.objList:
			o.tellCurrentObjects(self.arcs, self.rects)
			o.update()

	def handleFriction(self):
		try:
			for o in self.objList:
				if not o.isMoving:
					o.velocity.setX(o.velocity.x * self.friction)
					o.accel.setX(0)
		except AttributeError:
			pass

	def steer(self, k, b):
		for o in self.objList:
			o.steer(k, b)
