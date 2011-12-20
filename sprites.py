import pygame
from pygame.locals import *

class player(pygame.sprite.Sprite):
	'''
	Class to handle several players
	'''
	def __init__(self, posX, posY, path2pic):
		pygame.sprite.Sprite.__init__(self)
		i = handleImg()

		self.image, self.rect = i.load_image(path2pic, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY

		self.speed = 4
		self.isMoving = False

	def update(self):
		if self.isMoving:
			self._move(self.speed)

	def _move(self, mover):
		newpos = self.rect.move((mover, 0))
		if not self.area.contains(newpos):
			print "Moved outside of the screen..."
		self.rect = newpos

	def steer(self, button, move):
		if move:
			self.isMoving = True
			if button == 97: # a
				if self.speed > 0:
					self.speed = -self.speed
			elif button == 100: # d
				if self.speed < 0:
					self.speed = -self.speed
		else:
			self.isMoving = False


class handleImg(object):
	def load_image(self, path, colorkey=None):
		try:
			image = pygame.image.load(path)
		except pygame.error, message:
			print 'Cannot load image:', path
			raise SystemExit, message
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
				image.set_colorkey(colorkey, RLEACCEL)
		return image, image.get_rect()




