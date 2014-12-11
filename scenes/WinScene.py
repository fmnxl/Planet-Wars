import pygame
from pygame.locals import *
from scenes.Scene import Scene
from config.Config import *

class WinScene(Scene):
	def __init__(self):
		super(WinScene, self).__init__()
		self.rendered = False

	def render(self, screen):
		if self.rendered:
			return

		font = pygame.font.Font(Config.getFile(Config.ethnocentric), 50)
		text = font.render("YOU WON", True, (255,255,255))
		textRect = text.get_rect()
		textRect.center = screen.get_rect().center
		screen.blit(text, textRect)

		font = pygame.font.Font(Config.getFile(Config.ethnocentric), 20)
		text = font.render("PRESS ANY KEY TO CONTINUE", True, (255,255,255))
		textRect = text.get_rect()
		textRect.center = screen.get_rect().center
		textRect.y += 70
		screen.blit(text, textRect)

		pygame.display.flip()
		self.rendered = True

	def update(self, deltaTime):
		pass

	def handleEvents(self, events, keys):
		for event in events:
			if event.type == KEYDOWN:
				from scenes.TitleScene import TitleScene
				self.manager.goTo(TitleScene())