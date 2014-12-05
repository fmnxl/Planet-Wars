import pygame
from scenes.title.Menu import *
from scenes.GameScene import *
from models.SavedGame import *

class SavedGamesMenu(Menu):
	def __init__(self):
		super(SavedGamesMenu, self).__init__()
		self.selections = ["BACK"]

		# load saved games
		self.savedGames = SavedGame.loadAll()

		for savedGame in self.savedGames:
			self.selections.append(savedGame.name)


	def doSelect(self, index):
		if index == 0:
			from scenes.title.MainMenu import *
			self.manager.goTo(MainMenu())
		elif index < len(self.selections):
			self.manager.scene.goToGameScene(self.savedGames[index - 1])