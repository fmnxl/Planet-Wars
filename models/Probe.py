import pygame, pygame.mixer
from lib.euclid import *
from models.Bullet import *

class Probe(object):
	def __init__(self, position, speed):
		self.position = position
		self.speed = speed
		self.maxSpeed = 10
		self.maxSpeedSquared = self.maxSpeed ** 2
		self.thrust = 0.025
		self.fuelEfficiency = 1
		self.fuelCapacity = 1500.0
		self.direction = 180
		self.gravitationalPull = Vector2(0,0)
		self.directionChange = 0
		self.acceleration = Vector2(0,0)

		self.imageSize = Vector2(1.73, 2.91) #* 4.0/3.0
		self.size = 1.0 # for collision purpose

		self.originalImage = pygame.image.load("img/rocket4.png").convert_alpha()
		self.zoom = 0

		self.zoomedImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * self.zoom)))
		self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
		self.rect = self.tempImage.get_rect()

		self.fuel = 100
		self.maxHealth = 200
		self.health = self.maxHealth
		self.isHit = False

		self.bullets = []
		self.fireTemp = 0
		self.score = 0

		self.thrustSound = pygame.mixer.Sound("sound/thrust.ogg")
		self.soundChannel = pygame.mixer.Channel(1)
		self.soundIsPlaying = False
		

	def listenToKeyboard(self, keys):
		self.acceleration = Vector2(0,0)
		if keys[pygame.K_w] or keys[pygame.K_s]:
			self.acceleration = self.thrust * Vector2(math.sin(math.radians(self.direction)), math.cos(math.radians(self.direction)))
			if keys[pygame.K_s]:
				self.acceleration = -1 * self.acceleration
			self.fuel -= self.fuelEfficiency * self.thrust
			self.speed -= self.acceleration
			if(self.speed.magnitude_squared() > self.maxSpeedSquared):
				self.speed = self.speed.normalize() * self.maxSpeed
		if keys[pygame.K_a] or keys[pygame.K_d]:
			self.acceleration = self.thrust * Vector2(math.sin(math.radians(self.direction + 90)), math.cos(math.radians(self.direction + 90)))
			if keys[pygame.K_d]:
				self.acceleration = -1 * self.acceleration
			self.fuel -= self.fuelEfficiency * self.thrust
			self.speed -= self.acceleration
			if(self.speed.magnitude_squared() > self.maxSpeedSquared):
				self.speed = self.speed.normalize() * self.maxSpeed
		if keys[pygame.K_q]:
		    self.directionChange = 100
		if keys[pygame.K_e]:
		    self.directionChange = -100
		if keys[pygame.K_SPACE]:
		    self.fire()

		if keys[pygame.K_1]:
		    self.thrust = 0.025 * 1
		elif keys[pygame.K_2]:
		    self.thrust = 0.025 * 2
		elif keys[pygame.K_3]:
		    self.thrust = 0.025 * 3
		elif keys[pygame.K_4]:
		    self.thrust = 0.025 * 4
		elif keys[pygame.K_5]:
		    self.thrust = 0.025 * 5
		elif keys[pygame.K_5]:
		    self.thrust = 0.025 * 5
		elif keys[pygame.K_6]:
		    self.thrust = 0.025 * 6
		elif keys[pygame.K_7]:
		    self.thrust = 0.025 * 7
		elif keys[pygame.K_8]:
		    self.thrust = 0.025 * 8
		elif keys[pygame.K_9]:
		    self.thrust = 0.025 * 9
		elif keys[pygame.K_0]:
		    self.thrust = 0.025 * 20


	def update(self, deltaTime):

		if (not self.soundChannel.get_busy()) and self.acceleration != Vector2(0,0):
			self.soundChannel.play(self.thrustSound)
			self.soundChannel.set_volume(10 * self.thrust)
		elif self.soundChannel.get_busy() and self.acceleration == Vector2(0,0):
			self.soundChannel.set_volume(self.soundChannel.get_volume() - 0.6 * deltaTime)
			if self.soundChannel.get_volume() <= 0.0:
				self.soundChannel.stop()
		# deltaTimeSmall = deltaTime
		self.speed += self.gravitationalPull * deltaTime
		self.position += self.speed * deltaTime
		self.gravitationalPull = Vector2(0,0)
		self.direction += self.directionChange * deltaTime
		for bullet in self.bullets:
			bullet.update(deltaTime)
			if bullet.checkReach() == False:
				self.bullets.remove(bullet)
		
	def blit(self, screen, camera):
		if self.zoom != camera.zoom:
			self.zoomedImage = pygame.transform.smoothscale(self.originalImage, map(int, (self.imageSize * camera.zoom)))
			self.tempImage = pygame.transform.rotate(self.zoomedImage, self.direction)
			# self.tempImage = pygame.transform.rotozoom(self.originalImage, self.direction, camera.zoom / 100.0)
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

		maxWidth = 0.02 * camera.zoom  * self.maxHealth
		healthRect = pygame.Rect((self.rect.topleft), (maxWidth, 2))
		healthRect.bottom = self.rect.top - 4
		healthRect.centerx = self.rect.centerx
		oldLeft = healthRect.left

		healthRect.width = maxWidth * self.health / self.maxHealth
		healthRect.left = oldLeft
		pygame.draw.rect(screen, (0,255,0), healthRect, 0)

		font = pygame.font.Font("font/ethnocentric.ttf", int(round(0.4 * camera.zoom)))
		text = font.render("HP:" + str(self.health), True, (255,255,255))
		textRect = text.get_rect()
		textRect.left = healthRect.left
		textRect.bottom = healthRect.top - 1
		screen.blit(text, textRect)

		


	def fire(self):
		self.fireTemp += 1
		if (self.fireTemp) % 5 == 0:
			bullet = Bullet(self.direction, self.position, self.speed, 30)
			self.bullets.append(bullet)

	def checkBulletHit(self, aliens, camera):
		for alien in aliens:
			for bullet in self.bullets:
				if bullet.checkHit(alien, camera):
					self.score += 1
					alien.alert = True
					self.bullets.remove(bullet)

	def shouldDie(self):
		return (self.health <= 0 or self.fuel <= 0)