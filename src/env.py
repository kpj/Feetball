import sprites

class world(object):
	'''
	Class to react to the environment
	'''
	def __init__(self, width, height):
		self.gravity = 9.81
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
		self.handleFriction()

	def update(self):
		for o in self.objList:
			o.update()

	def handleFriction(self):
		try:
			for o in self.objList:
				if not o.isMoving:
					o.velocity.setX(0)
					o.accel.setX(0)
		except AttributeError:
			pass

	def steer(self, k, b):
		for o in self.objList:
			o.steer(k, b)

	def checkCollision(self):
		tmp = []
		for o in self.objList:
			tmp = self.objList[:]
			tmp.remove(o)
			o.collide(tmp)
