import shelve
from datetime import datetime
from models.Alien import *
from config.Config import *

class SavedGame(object):
	@staticmethod
	def loadAll():
		db = shelve.open(Config.savedGamesDB)
		savedGames = db["savedGames"]
		db.close()
		return savedGames

	def __init__(self, name, planets, probe, aliens):
		self.name = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
		self.planets = [{
			"angle": planet.angleToCenter
		} for planet in planets]
		self.probe = {
			"position": probe.position,
			"speed": probe.speed,
			"health": probe.health,
			"fuel": probe.fuel,
			"score": probe.score,
			"direction": probe.direction
		}
		self.aliens = [{
			"position": alien.position,
			"speed": alien.speed,
			"health": alien.health
		} for alien in aliens]

	# restores game state from a SavedGame object
	def loadTo(self, planets, probe, aliens):
		# planets
		for i, planet in enumerate(planets):
			planet.angleToCenter = self.planets[i]["angle"]

		# probe
		probe.position = self.probe["position"]
		probe.speed = self.probe["speed"]
		probe.health = self.probe["health"]
		probe.fuel = self.probe["fuel"]
		probe.score = self.probe["score"]
		probe.direction = self.probe["direction"]

		#aliens
		del aliens[:] # remove all aliens from list while maintaining pointer
		for i, alien in enumerate(self.aliens):
			newAlien = Alien(alien["position"], alien["speed"], probe)
			newAlien.health = alien["health"]
			aliens.append(newAlien)

	def save(self):
		s = shelve.open(Config.savedGamesDB)
		appended = s["savedGames"]
		appended.append(self)
		s["savedGames"] = appended
		s.close()