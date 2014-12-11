from scenes.WinScene import WinScene

class LevelManager(object):
	def __init__(self, initialLevel, planets, probe, aliens, scene):
		self.planets = planets
		self.probe = probe
		self.aliens = aliens
		self.scene = scene
		self.goTo(initialLevel)

	def goTo(self, level):
		self.level = level
		self.level.planets = self.planets
		self.level.probe = self.probe
		self.level.aliens = self.aliens
		self.level.manager = self
		self.level.initialise()

	def goToWinScene(self):
		self.scene.manager.goTo(WinScene())