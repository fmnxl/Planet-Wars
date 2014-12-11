import pygame, math, random
from lib.euclid import *
from models.Bullet import Bullet
from config.Config import Config
from models.Vehicle import Vehicle

class Alien(Vehicle):
	def __init__(self, position, speed, enemy):
		super(Alien, self).__init__(position, speed, 0, Vector2(2,1), 1.0, "img/ufo.png", 100, 100, 0.5)

		self.fireRangeRadius = 20
		self.detectionRadius = 20

		self.fireTemp = 0

		self.enemy = enemy
		self.alert = False

	def update(self, deltaTime):
		super(Alien, self).update(deltaTime)
		
		# set behaviour towards enemy
		if self.enemy is not None:
			self.fireAt(self.enemy)
			self.chase(self.enemy, deltaTime)


	def render(self, screen, camera):
		super(Alien, self).render(screen, camera)
		

	def fireAt(self, enemy):
		self.fireTemp += 1
		if (self.fireTemp) % 20 == 1:
			v = self.position - enemy.position
			if v.magnitude() <= self.fireRangeRadius:
				angle = math.degrees(math.atan2(v[0], v[1]))
				angle += random.randrange(-20, 20)
				bullet = Bullet(angle, self.position, self.speed, 50)
				self.bullets.append(bullet)

	def chase(self, enemy, deltaTime):
		v = enemy.position - self.position
		if self.alert or v.magnitude() <= self.detectionRadius:
			bv =  enemy.position - v.normalize() * 14
			v2bv = bv - self.position
			if v2bv.magnitude_squared() > 9:
				change = v2bv.normalize() * 3.0 * self.thrust
				self.position += change * deltaTime
				self.speed = change
			else:
				self.position += v2bv * deltaTime
				self.speed = Vector2(0,0)

	def checkBulletHit(self, other, camera):
		for bullet in self.bullets:
			if bullet.checkHit(other, camera):
				self.bullets.remove(bullet)