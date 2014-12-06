import pygame, random, pygame.gfxdraw, sys, shelve
from pygame.locals import *
from lib.euclid import *
from config.Config import *
from scenes.Scene import Scene
from scenes.GameScene import GameScene
from models.SavedGame import *
from scenes.title.MainMenu import *

class MenuManager(object):
	def __init__(self, initialMenu, scene):
		self.goTo(initialMenu)
		self.scene = scene

	def goTo(self, menu):
		self.menu = menu
		self.menu.manager = self

class TitleScene(Scene):
	def __init__(self):
		super(TitleScene, self).__init__()

		# generate bg stars
		self.bgStars = []
		for i in range(0, 100):
			self.bgStars.append(Vector2(random.randrange(0, Config.screenWidth), random.randrange(0, Config.screenHeight)))

		# menu manager
		self.menuManager = MenuManager(MainMenu(), self)
		
	def update(self, deltaTime):
		pass

	def render(self, screen):
		screen.fill((0,0,0))

		# render bg stars
		for star in self.bgStars:
			position = map(int, star)
			randomVal = random.randrange(150, 255)
			color = (randomVal,randomVal,randomVal)
			pygame.gfxdraw.pixel(screen, position[0], position[1], (randomVal,randomVal,randomVal))

		# Render Game title
		titleFont = pygame.font.Font(Config.getFile(Config.ethnocentric), 80)
		titleText = titleFont.render("PLANET WARS", True, (255,255,255))
		titleTextRect = titleText.get_rect()
		titleTextRect.centerx = screen.get_rect().centerx
		titleTextRect.y = 40
		screen.blit(titleText, titleTextRect)

		# Render Menu
		self.menuManager.menu.render(screen)

	# proceed to game scene - called by a menu
	def goToGameScene(self, savedGame = None):
		self.manager.goTo(GameScene(savedGame))

	def handleEvents(self, events, keys):
		self.menuManager.menu.handleEvents(events, keys)