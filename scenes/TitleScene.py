import pygame, random, pygame.gfxdraw, sys, shelve
from pygame.locals import *
from lib.euclid import *
from config.Config import *
from scenes.Scene import Scene
from scenes.GameScene import GameScene
from models.SavedGame import *

class TitleScene(Scene):
	def __init__(self):
		super(TitleScene, self).__init__()
		self.currentMenu = "title"
		self.currentSelection = 0
		self.selections = []
		self.bgStars = []
		self.selectionsRects = []
		for i in range(0, 100):
			self.bgStars.append(Vector2(random.randrange(0, Config.screenWidth), random.randrange(0, Config.screenHeight)))

		self.selectSound = pygame.mixer.Sound("sound/select.ogg")
		
	def update(self, deltaTime):
		pass


	def render(self, screen):
		screen.fill((0,0,0))
		WHITE = (255,255,255)

		# random stars
		for star in self.bgStars:
			position = map(int, star)
			randomVal = random.randrange(150, 255)
			color = (randomVal,randomVal,randomVal)
			pygame.gfxdraw.pixel(screen, position[0], position[1], (randomVal,randomVal,randomVal))

		# GUI

		titleFont = pygame.font.Font("font/ethnocentric.ttf", 80)
		titleText = titleFont.render("PLANET WARS", True, WHITE)
		titleTextRect = titleText.get_rect()
		titleTextRect.centerx = screen.get_rect().centerx
		titleTextRect.y = 40
		screen.blit(titleText, titleTextRect)

		if self.currentMenu == "title":
			

			self.selections = ["NEW GAME", "LOAD GAME", "HIGH SCORES", "QUIT"]
			selectionsTexts = []
			selectionsRects = []

			menuFont = pygame.font.Font("font/ethnocentric.ttf", 40)
			for index, item in enumerate(self.selections):
				text = menuFont.render(item, True, WHITE)
				textRect = text.get_rect()
				textRect.centerx = screen.get_rect().centerx
				textRect.y = 180 + index * 60
				selectionsTexts.append(text)
				selectionsRects.append(textRect)

			self.selectionsRects = selectionsRects

			highlightRect = selectionsRects[self.currentSelection].copy()
			highlightRect.height = 2
			highlightRect.top = selectionsRects[self.currentSelection].bottom
			pygame.draw.rect(screen, (0,254,253), highlightRect, 0)

			for i, text in enumerate(selectionsTexts):
					screen.blit(text, selectionsRects[i])
		
		elif self.currentMenu == "saved_games":
			selectionsTexts = []
			selectionsRects = []
			self.selections = ["BACK"]
			menuFont = pygame.font.Font("font/ethnocentric.ttf", 40)
			text = menuFont.render("BACK", True, WHITE)
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().centerx
			textRect.y = 180
			selectionsTexts.append(text)
			selectionsRects.append(textRect)

			for i, savedGame in enumerate(self.savedGames):
				text = menuFont.render(savedGame.name, True, WHITE)
				textRect = text.get_rect()
				textRect.centerx = screen.get_rect().centerx
				textRect.y = 240 + i * 60
				self.selections.append(savedGame.name)
				selectionsTexts.append(text)
				selectionsRects.append(textRect)

			self.selectionsRects = selectionsRects

			highlightRect = selectionsRects[self.currentSelection].copy()
			highlightRect.height = 2
			highlightRect.top = selectionsRects[self.currentSelection].bottom
			pygame.draw.rect(screen, (0,254,253), highlightRect, 0)

			for i, text in enumerate(selectionsTexts):
				screen.blit(text, selectionsRects[i])


	def selectOnMainMenu(self):
		if self.currentMenu == "title":
			if self.currentSelection == 0:
				self.manager.go_to(GameScene())
			elif self.currentSelection == 1:
				s = shelve.open('saved_games.db')
				self.savedGames = s["savedGames"]
				s.close()
				self.currentMenu = "saved_games"
				self.currentSelection = 0
			elif self.currentSelection == 2:
				s = shelve.open('saved_games.db')
				s["savedGames"] = []
				s.close()
			elif self.currentSelection == 3:
				pygame.quit()
				sys.exit()
		elif self.currentMenu == "saved_games":
			if self.currentSelection == 0:
				self.currentMenu = "title"
			elif self.currentSelection < len(self.selections):
				self.manager.go_to(GameScene(self.savedGames[self.currentSelection - 1]))
	def handleEventsMainMenu(self, events, keys):
		
		mousePos = pygame.mouse.get_pos()

		for event in events:
			if event.type == MOUSEBUTTONUP:
				for i, rect in enumerate(self.selectionsRects):
					if rect.collidepoint(mousePos):
						self.selectOnMainMenu()
			if event.type == MOUSEMOTION:
				for i, rect in enumerate(self.selectionsRects):
					if rect.collidepoint(mousePos) and i != self.currentSelection:
						self.selectSound.play()
						self.currentSelection = i
			if event.type == KEYDOWN:
				if event.key == K_DOWN and self.currentSelection < len(self.selections) - 1:
					self.selectSound.play()
					self.currentSelection += 1
				if event.key == K_UP and self.currentSelection > 0:
					self.selectSound.play()
					self.currentSelection -= 1
				
				if event.key == K_RETURN or event.key == K_SPACE:
					self.selectOnMainMenu()

		if self.currentMenu == "title":
			for event in events:
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE and self.currentSelection != 3:
						self.selectSound.play()
						self.currentSelection = 3

		if self.currentMenu == "saved_games":
			for event in events:
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE and self.currentSelection != 0:
						self.selectSound.play()
						self.currentSelection = 0

	def handleEvents(self, events, keys):
		# if self.currentMenu == "title":
		self.handleEventsMainMenu(events, keys)