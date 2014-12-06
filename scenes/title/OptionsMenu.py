import pygame, sys
from pygame.locals import *
from config.Config import *
from scenes.title.Menu import *
from scenes.title.SavedGamesMenu import *

class OptionsMenu(Menu):
	def __init__(self):
		super(OptionsMenu, self).__init__()
		self.selections = ["SAVE & BACK", "RESOLUTION", "FULLSCREEN"]

		self.modes = pygame.display.list_modes(32)
		self.fullscreen = Config.fullscreen

	def doSelect(self, index):
		if index == 0:
			pygame.display.set_mode(self.modes[Config.screenMode], Config.getScreenFlags())
			from scenes.title.MainMenu import *
			self.manager.goTo(MainMenu())

	def changeSettings(self, index, left):
		if index == 1:
			if Config.screenMode > 0 and left:
				Config.screenMode -= 1
			if Config.screenMode < len(self.modes) - 1 and not left:
				Config.screenMode += 1

		elif index == 2:
			Config.fullscreen = not Config.fullscreen


	def handleEvents(self, events, keys):
		super(OptionsMenu, self).handleEvents(events, keys)

		for event in events:
			# Keyboard Events
			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					self.selectSound.play()
					self.changeSettings(self.currentSelection, True)
				if event.key == K_RIGHT:
					self.selectSound.play()
					self.changeSettings(self.currentSelection, False)


	def render(self, screen):
		selectionsTexts = []
		selectionsRects = []
		menuFont = pygame.font.Font(Config.getFile(Config.ethnocentric), 40)

		for i, selection in enumerate(self.selections):
			text = menuFont.render(selection, True, (255,255,255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().width / 4 if i != 0 else screen.get_rect().centerx
			textRect.y = 180 + i * 60
			selectionsTexts.append(text)
			selectionsRects.append(textRect)

		for i, selection in enumerate(self.selections):
			if i == 1:
				value = str(self.modes[Config.screenMode])
			elif i == 2:
				value = "YES" if Config.fullscreen else "NO"
			else:
				continue
			text = menuFont.render(value, True, (255,255,255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().width / 4 * 3
			textRect.y = 180 + i * 60
			selectionsTexts.append(text)
			selectionsRects.append(textRect)

		self.selectionsRects = selectionsRects

		highlightRect = selectionsRects[self.currentSelection].copy()
		highlightRect.height = 2
		highlightRect.top = selectionsRects[self.currentSelection].bottom
		pygame.draw.rect(screen, (0,254,253), highlightRect, 0)

		for i, text in enumerate(selectionsTexts):
			screen.blit(text, selectionsRects[i])