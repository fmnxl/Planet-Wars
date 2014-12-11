import pygame
from lib.euclid import Vector2
from config.Config import Config

class Vehicle(object):
	def __init__(self, position, speed, direction, imageSize, size, imageFile, health, maxHealth, thrust):
		self.position = position
		self.speed = speed
		self.direction = direction
		self.gravitationalPull = Vector2(0,0)
		self.directionChange = 0
		self.thrust = thrust

		self.imageSize = imageSize
		self.size = size # for collision purpose

		self.originalImage = pygame.image.load(Config.getFile(imageFile)).convert_alpha()
		self.zoom = 0

		self.zoomedImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * self.zoom)))
		self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
		self.rect = self.tempImage.get_rect()

		self.maxHealth = maxHealth
		self.health = health
		self.isHit = False

		self.bullets = []

	def update(self, deltaTime):
		self.speed += self.gravitationalPull * deltaTime
		self.position += self.speed * deltaTime
		self.gravitationalPull = Vector2(0,0)
		self.direction += self.directionChange * deltaTime

		for bullet in self.bullets:
			bullet.update(deltaTime)
			if bullet.checkReach() == False:
				self.bullets.remove(bullet)


	def render(self, screen, camera):
		if self.zoom != camera.zoom:
			self.zoomedImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * camera.zoom)))
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			self.rect = self.tempImage.get_rect()

			self.zoom = camera.zoom

		if abs(self.directionChange) > 0:
			oldCenter = self.rect.center
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			self.rect = self.tempImage.get_rect()
			self.rect.center = oldCenter

			self.directionChange = 0

		if self.isHit:
			self.tempImage.fill((255,0,0), special_flags=pygame.BLEND_RGBA_MULT)

		self.rect.center = camera.convertCoordinates(self.position)
		screen.blit(self.tempImage, self.rect)

		if self.isHit:
			self.zoomedImage = pygame.transform.scale(self.originalImage, map(int, (self.imageSize * camera.zoom)))
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			self.isHit = False
			
		for bullet in self.bullets:
			bullet.blit(screen, camera)

		# health bar and info
		maxWidth = 0.02 * camera.zoom  * self.maxHealth
		healthRect = pygame.Rect((self.rect.topleft), (maxWidth, 2))
		healthRect.bottom = self.rect.top - 4
		healthRect.centerx = self.rect.centerx
		oldLeft = healthRect.left

		healthRect.width = maxWidth * self.health / self.maxHealth
		healthRect.left = oldLeft
		pygame.draw.rect(screen, (0,255,0), healthRect, 0)

		font = pygame.font.Font(Config.getFile(Config.ethnocentric), int(round(0.4 * camera.zoom)))
		text = font.render("HP:" + str(self.health), True, (255,255,255))
		textRect = text.get_rect()
		textRect.left = healthRect.left
		textRect.bottom = healthRect.top - 1
		screen.blit(text, textRect)