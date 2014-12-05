import pygame, sys
from scenes.title.Menu import *
from scenes.title.SavedGamesMenu import *
from scenes.title.OptionsMenu import *
from scenes.title.ControlsMenu import *

class MainMenu(Menu):
	def __init__(self):
		super(MainMenu, self).__init__()
		self.selections = ["NEW GAME", "LOAD GAME", "HIGH SCORES", "OPTIONS", "CONTROLS", "QUIT"]

	def doSelect(self, index):
		if index == 0:
			self.manager.scene.goToGameScene()
		elif index == 1:
			self.manager.goTo(SavedGamesMenu())
		elif index == 2:
			s = shelve.open('saved_games.db')
			s["savedGames"] = []
			s.close()
		elif index == 3:
			self.manager.goTo(OptionsMenu())
		elif index == 4:
			self.manager.goTo(ControlsMenu())
		elif index == 5:
			pygame.quit()
			sys.exit()