import pygame, pygame.gfxdraw
from lib.euclid import *
from models.HeavenlyBody import HeavenlyBody
from config.Config import *

class Sun(HeavenlyBody):
	def __init__(self):
		self.mass = 33300
		self.position = Vector2(0,0)
		self.size = 15

		self.imageSize = Vector2(self.size*2, self.size*2)
		self.zoom = 0
		self.originalImage = pygame.image.load(Config.getFile("img/planets/sun.png")).convert_alpha()
		self.tempImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * self.zoom)))
		self.rect = self.tempImage.get_rect()

	def blit(self, screen, camera):
		v = camera.convertCoordinates(self.position)
		# pygame.draw.circle(screen, (255,255,0), v, int(self.size * camera.zoom), 0)
		# try:
		# 	pygame.gfxdraw.aacircle(screen, v.x, v.y, int(round(self.size * camera.zoom)), (255,255,0))
		# 	pygame.gfxdraw.filled_circle(screen, v.x, v.y, int(round(self.size * camera.zoom)), (255,255,0))
		# except:
		# 	pass

		if self.zoom != camera.zoom:
			self.tempImage = pygame.transform.scale(self.originalImage, map(int, (self.imageSize * camera.zoom)))
			self.rect = self.tempImage.get_rect()
			self.zoom = camera.zoom

		self.rect.center = camera.convertCoordinates(self.position)
		screen.blit(self.tempImage, self.rect)