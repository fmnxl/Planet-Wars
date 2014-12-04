from lib.euclid import *

class HeavenlyBody(object):
	def attractMulti(self, others):
		for other in others:
			self.attract(other)

	def attract(self, other):
		G = 0.003
		gravitationalPull = Vector2(0,0)
		distance = self.position - other.position
		other.gravitationalPull += G * self.mass / distance.magnitude_squared() * distance.normalize()
		
	def checkCollisionMulti(self, others):
		for other in others:
			self.checkCollision(other)

	def checkCollision(self, other):
		v = other.position - self.position
		if v.magnitude() <= self.size + other.size:
			return True
		return False
