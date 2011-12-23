import pygame, os
from pygame.locals import *
from sprites import *
from env import *

class setupWindow(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.clock = pygame.time.Clock()
		self.s = keySet()
		self.world = world(width, height - 50)

	def init(self, title):
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(title)
		pygame.mouse.set_visible(False)

	def setBG(self, color):
		self.bg = pygame.Surface(self.screen.get_size())
		self.bg = self.bg.convert()
		self.bg.fill(color)

		self.screen.blit(self.bg, (0, 0))
		pygame.display.flip()

	def addSpheres(self):
		p = [
			[150, self.height - 120, os.path.join('img', 'p1.png'), self.s.getSet(0), 10, True],
			[self.width - 200, self.height - 120, os.path.join('img', 'p2.png'), self.s.getSet(1), 10, True],
			[self.width/2, 50, os.path.join('img', 'ball.png'), self.s.getSet(1), 8, False]
		]

		for i in p:
			self.world.addObject(sphere(*i))

	def addWalls(self):
		w = [
			[50, self.height - 50, os.path.join('img', 'bottom.png')],
			[0, self.height - 150, os.path.join('img', 'chest.png')],
			[self.width - 100, self.height - 150, os.path.join('img', 'chest.png')],
			[0, self.height - 250, os.path.join('img', 'chest.png')],
			[self.width - 100, self.height - 250, os.path.join('img', 'chest.png')]
		]

		for i in w:
			self.world.addObject(wall(*i))

	def game(self):
		objT = tuple(self.world.getObjects())
		allsprites = pygame.sprite.RenderUpdates(objT)

		running = True
		while running:
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

			self.screen.blit(self.bg, (0, 0))
			allsprites.draw(self.screen)

			pygame.display.flip()

		print "Aborting game..."
