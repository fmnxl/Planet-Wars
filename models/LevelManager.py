class LevelManager(object):
	def __init__(self, initialLevel, planets, probe, aliens):
		self.planets = planets
		self.probe = probe
		self.aliens = aliens
		self.levelNum = 1
		self.goTo(initialLevel)

	def goTo(self, level):
		self.level = level
		self.level.planets = self.planets
		self.level.probe = self.probe
		self.level.aliens = self.aliens
		self.level.manager = self
		self.level.initialise()