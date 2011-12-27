import pygame, os, time
from pygame.locals import *
from sprites import *
from env import *
from var import *
from useful import *
import objects

class setupWindow(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.clock = pygame.time.Clock()
		self.s = keySet()
		self.world = world(width, height)

	def init(self, title):
		pygame.init()
#		pygame.mixer.init()

		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(title)
		pygame.mouse.set_visible(False)

		self.font = pygame.font.Font(None, 36)
		self.fontSmall = pygame.font.Font(None, 18)

	def setBG(self, color):
		self.bg = pygame.Surface(self.screen.get_size())
		self.bg = self.bg.convert()
		self.bgColor = color

	def updateBG(self):
		self.bg.fill(self.bgColor)

	def addSpheres(self):
		for i in objects.p:
			self.world.addObject(sphere(*i), "SPHERE")

	def addFeet(self):
		for i in objects.f:
			self.world.addObject(foot(*i), "FOOT")

	def addWalls(self):
		for i in objects.w:
			self.world.addObject(wall(*i), "RECT")

	def renderText(self, text, pos, small = False):
		if small:
			text = self.fontSmall.render(text, 1, (10, 10, 10))
		else:
			text = self.font.render(text, 1, (10, 10, 10))
		textpos = text.get_rect(center=(pos.x,pos.y)) # topleft=(pos.x,pos.y)
		self.bg.blit(text, textpos)

	def printResult(self, res):
		p = vector(WINDOWW/6.0, WINDOWH/10.0)
		for n,i in res.iteritems():
			self.renderText("%s: %s"%(n, i), p)
			p += vector(WINDOWW/2.0, 0)
		if self.oldResult != res:
			# A new score has been achieved + printed (delete old one)
			self.scoredGoal = True
			self.scoredGoalTime = time.time()
		self.oldResult = res

	def handleTimeLine(self):
		runTime = self.curTime - self.timerStart
		runTime *= 10 # Just scaling
		runHeight = 3

		if self.timer2right:
			startX = 0
			endX = runTime
			col = pygame.Color("red")
		else:
			startX = self.width
			endX = self.width - runTime
			col = pygame.Color("blue")

		pygame.draw.line(self.bg, col, (startX, runHeight), (endX, runHeight), 8)

		if self.timer2right and runTime >= self.width:
			# Now moves to the left side
			self.timerStart = self.curTime
			runTime = self.curTime - self.timerStart
			self.timer2right = False
		if not self.timer2right and runTime >= self.width:
			# Now moves to the right side
			self.timerStart = self.curTime
			runTime = self.curTime - self.timerStart
			self.timer2right = True

		# Show the time
		self.renderText(str(round(self.curTime - self.startTime, 2)), vector(endX, runHeight + 15), True)

	def createPowerUp(self):
		c = random.choice(objects.u.keys())
		# Nice position on the field
		xx = random.uniform(400.0, WINDOWW - 400.0)
		yy = random.uniform(900.0, WINDOWH - 800.0)
#		print c,objects.u[c][0]
		pu = powerup(xx, yy, os.path.join('img', 'powerup.png'), c, objects.u[c][0], objects.u[c][1])
		self.world.addObject(pu, "POWERUP")
		self.allsprites.add(pu)

	def checkUsedPowerUps(self):
		for o in self.world.powerups:
			if o.taken:
				# Has been used
				if o.destruct:
					# Duration is over
					self.allsprites.remove(o)
				else:
					# Just put me away, but don't kill
					o.rect.center = (-1000, -1000)

	def handlePowerUps(self):
		if round((self.curTime - self.startTime), 2) % 10 == 0:
			self.createPowerUp()
		self.checkUsedPowerUps()

	def celebrateGoal(self):
		goalX = WINDOWW/2
		goalY = WINDOWH/2
		if time.time() - self.scoredGoalTime > self.celebrationDuration:
			self.scoredGoal = False
		self.renderText("GOAL", vector(goalX, goalY))
		for o in extras.createParticles(goalX, goalY, 4, 5, False):
			self.allparticles.add(o)

	def handleParticles(self):
		self.allparticles.update()
		for o in self.world.particles:
			# Add world generated particles to group
			self.allparticles.add(o)
			# Clear to avoid recursion
			self.world.particles = []

		# check for death
		for o in self.allparticles.sprites():
			if o.destruct:
				# Should be destroyed
				self.allparticles.remove(o)

	def initVariables(self):
		self.timerStart = self.startTime

		self.timer2right = True
		self.oldResult = self.world.getGoals()
		self.scoredGoal = False
		self.scoredGoalTime = 0
		self.celebrationDuration = 2

	def game(self):
		self.startTime = time.time()

		objT = tuple(self.world.getObjects())
		self.allsprites = pygame.sprite.RenderPlain(objT)
		self.allparticles = pygame.sprite.RenderUpdates()

		self.initVariables()

		running = True
		while running:
			self.clock.tick(60)
			self.curTime = time.time()

			for e in pygame.event.get():
				if e.type == QUIT:
					running = False

				if e.type == KEYDOWN:
					self.world.steer(e.key, True)
					if e.key == K_ESCAPE:
						running = False
				elif e.type == KEYUP:
					self.world.steer(e.key, False)

			self.updateBG()

			if self.scoredGoal:
				# There was goal (in the last 'self.celebrationDuration')
				self.celebrateGoal()
			self.world.makeStuff()
			self.printResult(self.world.getGoals())
			self.handleTimeLine()
			self.handlePowerUps()
			self.handleParticles()

			self.screen.blit(self.bg, (0, 0))
			self.allsprites.draw(self.screen)
			self.allparticles.draw(self.screen)
			pygame.display.flip()

		print "Aborting game..."
