import pygame, os
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

	def setBG(self, color):
		self.bg = pygame.Surface(self.screen.get_size())
		self.bg = self.bg.convert()
		self.bg.fill(color)

	def addSpheres(self):
		for i in objects.p:
			self.world.addObject(sphere(*i), "SPHERE")

	def addFeet(self):
		for i in objects.f:
			self.world.addObject(foot(*i), "FOOT")

	def addWalls(self):
		for i in objects.w:
			self.world.addObject(wall(*i), "RECT")

	def renderText(self, text, pos):
		text = self.font.render(text, 1, (10, 10, 10))
		textpos = text.get_rect(topleft=(pos.x,pos.y))
		return text, textpos

	def printResult(self, res):
		p = vector(WINDOWW/6.0, WINDOWH/10.0)
		for n,i in res.iteritems():
			text, textpos = self.renderText("%s: %s"%(n, i), p)
			self.bg.blit(text, textpos)
			p += vector(WINDOWW/2.0, 0)

	def game(self):
		objT = tuple(self.world.getObjects())
		allsprites = pygame.sprite.RenderUpdates(objT)

		running = True
		i=0
		while running:
			i+=1
			self.clock.tick(60)

			for e in pygame.event.get():
				if e.type == QUIT:
					running = False

				if e.type == KEYDOWN:
					self.world.steer(e.key, True)
					if e.key == K_ESCAPE:
						running = False
				elif e.type == KEYUP:
					self.world.steer(e.key, False)

			self.world.makeStuff()

			self.printResult(self.world.getGoals())

			self.screen.blit(self.bg, (0, 0))

			allsprites.draw(self.screen)

			pygame.display.flip()

		print "Aborting game..."
