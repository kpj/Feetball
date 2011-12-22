import pygame, sys, os
from pygame.locals import *
from sprites import *
from env import *

width = 600
height = 500

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('FeeterBall')
pygame.mouse.set_visible(1) # useless...

bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill((38, 255, 92))

screen.blit(bg, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

s = keySet()
w = world(width, height - 50)

w.addObject(
player(50, height - 100, os.path.join('img', 'p1.png'), s.getSet(0))
)
w.addObject(
player(width - 100, height - 100, os.path.join('img', 'p2.png'), s.getSet(1))
)

w.addObject(
wall(50, height - 50, os.path.join('img', 'bottom.png'))
)

objT = tuple(w.getObjects())
allsprites = pygame.sprite.RenderUpdates(objT)

running = True
while running:
	clock.tick(60)

	for e in pygame.event.get():
		if e.type == QUIT:
			running = False

		if e.type == KEYDOWN:
			w.steer(e.key, True)
			if e.key == K_ESCAPE:
				running = False
		elif e.type == KEYUP:
			w.steer(e.key, False)

		if e.type == MOUSEBUTTONDOWN:
			print pygame.mouse.get_pos()

	w.makeStuff()

	screen.blit(bg, (0, 0))
	allsprites.draw(screen)

	for o in w.getObjects():
		# For debugging
		try:
			pygame.draw.circle(screen, pygame.Color("black"), o.rect.center, o.r, 3)
		except AttributeError:
			pass

	pygame.display.flip()

print "Aborting game..."