import pygame, os
from pygame.locals import *
from sprites import *
from env import *
from var import *

class setupWindow(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.clock = pygame.time.Clock()
		self.s = keySet()
		self.world = world(width, height)

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
			[P1STARTX, P1STARTY, P1IMG, self.s.getSet(0), P1MASS, True, P1ID, P1NAME, PLAYERBOUNCE],
			[P2STARTX, P2STARTY, P2IMG, self.s.getSet(1), P2MASS, True, P2ID, P2NAME, PLAYERBOUNCE],
			[BALLSTARTX, BALLSTARTY, BALLIMG, None, BALLMASS, False, -1, "Hans", BALLBOUNCE]
		]

		for i in p:
			self.world.addObject(sphere(*i))

	def addWalls(self):
		w = [
			[50, self.height - 50, os.path.join('img', 'bottom.png'), True, -1],
			[0, self.height - 150, os.path.join('img', 'chest.png'), True, -1],
			[self.width - 100, self.height - 150, os.path.join('img', 'chest.png'), True, -1],
			[0, self.height - 250, os.path.join('img', 'chest.png'), True, -1],
			[self.width - 100, self.height - 250, os.path.join('img', 'chest.png'), True, -1],
			[self.width - 130, self.height - 150, os.path.join('img', 'goal.png'), False, P1ID],
			[100, self.height - 150, os.path.join('img', 'goal.png'), False, P2ID],
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
