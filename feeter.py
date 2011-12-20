import pygame, sys, os
from pygame.locals import *
from sprites import *

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

p1 = player(50, height - 100, os.path.join('img', 'p1.png'))
allsprites = pygame.sprite.RenderPlain((p1))

running = True
while running:
	clock.tick(60)

	for e in pygame.event.get():
		if e.type == QUIT:
			running = False
		elif e.type == KEYDOWN:
			p1.steer(e.key, True)
			if e.key == K_ESCAPE:
				running = False
		elif e.type == KEYUP:
			p1.steer(e.key, False)
		elif e.type == MOUSEBUTTONDOWN:
			print pygame.mouse.get_pos()

	allsprites.update()

	screen.blit(bg, (0, 0))
	allsprites.draw(screen)
	pygame.display.flip()
