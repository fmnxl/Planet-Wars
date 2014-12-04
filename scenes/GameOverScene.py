import pygame
from pygame.locals import *
from scenes.Scene import Scene

class GameOverScene(Scene):
	def __init__(self, lastCheckpoint, message = None):
		super(GameOverScene, self).__init__()
		self.rendered = False
		self.message = message

	def render(self, screen):
		# screen.fill((0, 0, 0))
		if self.rendered:
			return

		font = pygame.font.Font("font/ethnocentric.ttf", 50)
		text = font.render("GAME OVER", True, (255,255,255))
		textRect = text.get_rect()
		textRect.center = screen.get_rect().center
		screen.blit(text, textRect)

		y = 70

		if self.message is not None:
			font = pygame.font.Font("font/ethnocentric.ttf", 20)
			text = font.render(self.message, True, (255,255,255))
			textRect = text.get_rect()
			textRect.center = screen.get_rect().center
			textRect.y += y
			screen.blit(text, textRect)
			y += 65

		font = pygame.font.Font("font/ethnocentric.ttf", 20)
		text = font.render("PRESS ANY KEY TO CONTINUE", True, (255,255,255))
		textRect = text.get_rect()
		textRect.center = screen.get_rect().center
		textRect.y += y
		screen.blit(text, textRect)

		pygame.display.flip()
		self.rendered = True

	def update(self, deltaTime):
		pass

	def handleEvents(self, events, keys):
		for event in events:
			if event.type == KEYDOWN:
				from scenes.TitleScene import TitleScene
				self.manager.go_to(TitleScene())