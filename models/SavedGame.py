import shelve
from datetime import datetime
from models.Alien import *

class SavedGame(object):
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

	@classmethod
	def loadAllNames():
		s = shelve.open("saved_games.db")
		return [game.name for game in s["savedGames"]]
		s.close()

	# @classmethod
	# def loadWithName(name, planets, probe, aliens):
	# 	s = shelve.open("saved_games.db")
	# 	savedGames = s["savedGames"]
	# 	s.close()
	# 	for game in savedGames:
	# 		if game.name == name:
	# 			SavedGame.load(game, planets, probe, aliens)
	# 		return None
		

	# @classmethod
	# def loadWithIndex(index, planets, probe, aliens):
	# 	s = shelve.open("saved_games.db")
	# 	savedGames = s["savedGames"]
	# 	s.close()
	# 	SavedGame.load(savedGames[index], planets, probe, aliens)

	# @classmethod
	# def load(game, planets, probe, aliens):
	# 	for i, planet in enumerate(planets):
	# 		planet.angleToCenter = game.planets[i]["angle"]

	# 	probe.position = game.probe["position"]
	# 	probe.speed = game.probe["speed"]
	# 	probe.health = game.probe["health"]
	# 	probe.fuel = game.probe["fuel"]

	# 	for i, alien in enumerate(aliens):
	# 		alien.position = game.aliens[i]["position"]
	# 		alien.speed = game.aliens[i]["speed"]
	# 		alien.health = game.aliens[i]["health"]

	def loadTo(self, planets, probe, aliens):
		for i, planet in enumerate(planets):
			planet.angleToCenter = self.planets[i]["angle"]

		probe.position = self.probe["position"]
		probe.speed = self.probe["speed"]
		probe.health = self.probe["health"]
		probe.fuel = self.probe["fuel"]
		probe.score = self.probe["score"]
		probe.direction = self.probe["direction"]

		del aliens[:]
		for i, alien in enumerate(self.aliens):
			newAlien = Alien(alien["position"], alien["speed"], probe)
			newAlien.health = alien["health"]
			aliens.append(newAlien)

	def save(self):
		s = shelve.open("saved_games.db")
		appended = s["savedGames"]
		appended.append(self)
		s["savedGames"] = appended
		s.close()