from lib.euclid import Vector2

class HeavenlyBody(object):
	def attractMulti(self, others):
		for other in others:
			self.attract(other)

	def attract(self, other):
		G = 0.003
		gravitationalPull = Vector2(0,0)
		v = self.position - other.position
		distanceSq = v.magnitude_squared()
		if distanceSq > 0:
			other.gravitationalPull += G * self.mass / distanceSq * v.normalize()
		
	def checkCollisionMulti(self, others):
		for other in others:
			self.checkCollision(other)

	def checkCollision(self, other):
		v = other.position - self.position
		if v.magnitude() <= self.size + other.size:
			return True
		return False

	def render(self, screen, camera):
		raise NotImplementedError

	def update(self, deltaTime):
		raise NotImplementedError
