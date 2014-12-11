import pygame
from scenes.title.Menu import Menu
from scenes.GameScene import GameScene
from models.SavedGame import SavedGame
from config.Config import Config

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
			from scenes.title.MainMenu import MainMenu
			self.manager.goTo(MainMenu())
		elif index < len(self.selections):
			self.manager.scene.goToGameScene(self.savedGames[index - 1])

	def deleteSavedGame(self, index):
		savedGame = self.savedGames[index - 1]
		self.savedGames.remove(savedGame)
		self.selections.remove(self.selections[index])
		SavedGame.saveBulk(self.savedGames)

	def handleEvents(self, events, keys):
		super(SavedGamesMenu, self).handleEvents(events, keys)
		
		for event in events:
			# Keyboard Events
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					self.deleteSavedGame(self.currentSelection)

	def render(self, screen):
		super(SavedGamesMenu, self).render(screen)

		texts = []
		rects = []
		menuFont = pygame.font.Font(Config.getFile(Config.ethnocentric), 20)
	
		text = menuFont.render("ENTER - Load saved game", True, (255,255,255))
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().width / 4
		textRect.bottom = screen.get_rect().bottom - 20
		texts.append(text)
		rects.append(textRect)

		text = menuFont.render("BACKSPACE - Delete saved game", True, (255,255,255))
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().width / 4 * 3
		textRect.bottom = screen.get_rect().bottom - 20
		texts.append(text)
		rects.append(textRect)

		for i, text in enumerate(texts):
			screen.blit(text, rects[i])