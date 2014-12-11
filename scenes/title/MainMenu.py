import pygame, sys
from scenes.title.Menu import Menu
from scenes.title.SavedGamesMenu import SavedGamesMenu
from scenes.title.OptionsMenu import OptionsMenu
from scenes.title.ControlsMenu import ControlsMenu

class MainMenu(Menu):
	def __init__(self):
		super(MainMenu, self).__init__()
		self.selections = ["NEW GAME", "LOAD GAME", "OPTIONS", "CONTROLS", "QUIT"]

	def doSelect(self, index):
		if index == 0:
			self.manager.scene.goToGameScene()
		elif index == 1:
			self.manager.goTo(SavedGamesMenu())
		elif index == 2:
			self.manager.goTo(OptionsMenu())
		elif index == 3:
			self.manager.goTo(ControlsMenu())
		elif index == 4:
			pygame.quit()
			sys.exit()