import pygame, pygame.mixer, math
from lib.euclid import Vector2
from models.Bullet import Bullet
from models.Vehicle import Vehicle
from config.Config import Config

# ----------------------------------------------
# A Probe is the vehiclie of the main character
# ----------------------------------------------

class Probe(Vehicle):
	def __init__(self, position, speed):
		super(Probe, self).__init__(position, speed, 180, Vector2(1.73, 2.91), 1.0, "img/rocket4.png", 200, 200, 0.025)

		# physics
		self.maxSpeed = 10
		self.maxSpeedSquared = self.maxSpeed ** 2
		self.acceleration = Vector2(0,0)

		# fuel
		self.fuel = 100
		self.fuelEfficiency = 1
		self.fuelCapacity = 1000.0
		
		# bullets
		self.bullets = []
		self.score = 0

		# sounds
		self.thrustSound = pygame.mixer.Sound("sound/thrust.ogg")
		self.soundChannel = pygame.mixer.Channel(1)
		self.soundIsPlaying = False

		# firing mechanism
		self.fireRate = 5
		self.timeBetweenFires = 1.0 / self.fireRate
		self.nextFireCountdown = 0.0

	def applyThrust(self, acceleration):
		self.fuel -= self.fuelEfficiency * self.thrust
		self.speed -= acceleration

		# limit to max speed
		if(self.speed.magnitude_squared() > self.maxSpeedSquared):
			self.speed = self.speed.normalize() * self.maxSpeed

	def handleEvents(self, events, keys):
		self.acceleration = Vector2(0,0)
		
		# move
		if keys[pygame.K_w] or keys[pygame.K_s]:
			acceleration = self.thrust * Vector2(math.sin(math.radians(self.direction)), math.cos(math.radians(self.direction)))
			if keys[pygame.K_s]:
				acceleration = -1 * acceleration
			self.applyThrust(acceleration)
			self.acceleration = acceleration

		if keys[pygame.K_a] or keys[pygame.K_d]:
			acceleration = self.thrust * Vector2(math.sin(math.radians(self.direction + 90)), math.cos(math.radians(self.direction + 90)))
			if keys[pygame.K_d]:
				acceleration = -1 * acceleration
			self.applyThrust(acceleration)
			self.acceleration = acceleration

		# rotate
		if keys[pygame.K_q]:
		    self.directionChange = 100
		if keys[pygame.K_e]:
		    self.directionChange = -100
		
		# fire
		if keys[pygame.K_SPACE]:
		    self.fire()

		# thrust levels
		if keys[pygame.K_1]:
		    self.thrust = 0.05 * 1
		elif keys[pygame.K_2]:
		    self.thrust = 0.05 * 2
		elif keys[pygame.K_3]:
		    self.thrust = 0.05 * 3
		elif keys[pygame.K_4]:
		    self.thrust = 0.05 * 4
		elif keys[pygame.K_5]:
		    self.thrust = 0.05 * 5
		elif keys[pygame.K_5]:
		    self.thrust = 0.05 * 5
		elif keys[pygame.K_6]:
		    self.thrust = 0.05 * 6
		elif keys[pygame.K_7]:
		    self.thrust = 0.05 * 7
		elif keys[pygame.K_8]:
		    self.thrust = 0.05 * 8
		elif keys[pygame.K_9]:
		    self.thrust = 0.05 * 9


	def update(self, deltaTime):
		super(Probe, self).update(deltaTime)

		# thrust sound
		if (not self.soundChannel.get_busy()) and self.acceleration != Vector2(0,0):
			self.soundChannel.play(self.thrustSound)
			self.soundChannel.set_volume(10 * self.thrust)
		elif self.soundChannel.get_busy() and self.acceleration == Vector2(0,0):
			self.soundChannel.set_volume(self.soundChannel.get_volume() - 0.6 * deltaTime)
			if self.soundChannel.get_volume() <= 0.0:
				self.soundChannel.stop()

		# for fire rate
		if self.nextFireCountdown > 0:
			self.nextFireCountdown -= deltaTime
		
		if self.nextFireCountdown <= 0:
			self.nextFireCountdown = 0
		
	def render(self, screen, camera):
		super(Probe, self).render(screen, camera)

	def fire(self):
		# fire only if long enough since last fire
		if self.nextFireCountdown == 0:
			self.nextFireCountdown = self.timeBetweenFires
			bullet = Bullet(self.direction, self.position, self.speed, 30)
			self.bullets.append(bullet)

	# check if any bullets fired has hit any aliens
	def checkBulletHit(self, aliens, camera):
		for alien in aliens:
			for bullet in self.bullets:
				if bullet.checkHit(alien, camera):
					self.score += 1
					alien.alert = True
					self.bullets.remove(bullet)
