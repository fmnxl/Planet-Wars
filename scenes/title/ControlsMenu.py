import pygame, sys
from scenes.title.Menu import *
from scenes.title.SavedGamesMenu import *
from scenes.title.OptionsMenu import *

class ControlsMenu(Menu):
	def __init__(self):
		super(ControlsMenu, self).__init__()
		self.selections = ["BACK"]

		self.controls1 = [
			"W  MOVE FORWARD",
			"S  MOVE BACKWARD",
			"A  MOVE LEFT",
			"D  MOVE RIGHT",
			"Q  ROTATE ANTICLOCKWISE",
			"R  ROTATE CLOCKWISE"
			"SPACE FIRE"
		]
		self.controls2 = [
			"-  ZOOM OUT",
			"+  ZOOM IN",
			"F  TOGGLE CAMERA LOCK",
			"UP  MOVE CAMERA UP",
			"DOWN  MOVE CAMERA DOWN",
			"LEFT  MOVE CAMERA LEFT",
			"RIGHT  MOVE CAMERA RIGHT",
		]

	def doSelect(self, index):
		if index == 0:
			from scenes.title.MainMenu import *
			self.manager.goTo(MainMenu())

	def render(self, screen):
		super(ControlsMenu, self).render(screen)
		controlsTexts = []
		controlsRects = []
		menuFont = pygame.font.Font("font/ethnocentric.ttf", 15)

		for i, control in enumerate(self.controls1):
			text = menuFont.render(control, True, (255,255,255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().width / 4
			textRect.y = 250 + i * 60
			controlsTexts.append(text)
			controlsRects.append(textRect)

		for i, control in enumerate(self.controls2):
			text = menuFont.render(control, True, (255,255,255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().width / 4 * 3
			textRect.y = 250 + i * 60
			controlsTexts.append(text)
			controlsRects.append(textRect)

		for i, text in enumerate(controlsTexts):
			screen.blit(text, controlsRects[i])