import pygame
from pygame.locals import *
from config.Config import *

class Menu(object):
	def __init__(self):
		self.selections = []
		self.currentSelection = 0
		self.exitSelectionIndex = 0
		self.selectSound = pygame.mixer.Sound("sound/select.ogg")
		self.selectionsRects = []

	def doSelect(self, index):
		raise NotImplementedError

	def handleEvents(self, events, keys):
		mousePos = pygame.mouse.get_pos()

		for event in events:

			# Mouse Events
			if event.type == MOUSEBUTTONUP:
				for i, rect in enumerate(self.selectionsRects):
					if rect.collidepoint(mousePos):
						self.doSelect(self.currentSelection)
			if event.type == MOUSEMOTION:
				for i, rect in enumerate(self.selectionsRects):
					if rect.collidepoint(mousePos) and i != self.currentSelection:
						self.selectSound.play()
						self.currentSelection = i

			# Keyboard Events
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE and self.currentSelection != self.exitSelectionIndex:
					self.selectSound.play()
					self.currentSelection = self.exitSelectionIndex
				if event.key == K_DOWN and self.currentSelection < len(self.selections) - 1:
					self.selectSound.play()
					self.currentSelection += 1
				if event.key == K_UP and self.currentSelection > 0:
					self.selectSound.play()
					self.currentSelection -= 1
				
				if event.key == K_RETURN or event.key == K_SPACE:
					self.doSelect(self.currentSelection)

	def render(self, screen):
		selectionsTexts = []
		selectionsRects = []
		menuFont = pygame.font.Font(Config.getFile(Config.ethnocentric), 40)

		for i, selection in enumerate(self.selections):
			text = menuFont.render(selection, True, (255,255,255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().centerx
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