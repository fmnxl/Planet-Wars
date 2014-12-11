import pygame, random, pygame.mixer, pygame.gfxdraw, sys
from lib.euclid import Vector2
from config.Config import Config
from scenes.Scene import Scene
from scenes.GameScene import GameScene

class IntroScene(Scene):
	def __init__(self):
		super(IntroScene, self).__init__()

		# generate bg stars
		self.bgStars = []
		for i in range(0, 100):
			self.bgStars.append(Vector2(random.randrange(0, Config.getScreenSize()[0]), random.randrange(0, Config.getScreenSize()[1])))

		# bg music
		pygame.mixer.music.load(Config.getFile(Config.introBgMusic))
		pygame.mixer.music.play(-1) # loop forever

		# Render Lines
		self.fontColor = (255,255,0)
		self.titleFont = pygame.font.Font(Config.getFile(Config.ethnocentric), 40)
		self.font = pygame.font.Font(Config.getFile(Config.ethnocentric), 20)
		self.lineHeight = 55
		self.lines = [
			"HOME DEFENCE",
			"",
			"It is a period of space war. Alien",
			"spaceships, striking from a hidden base,",
			"have conquered the planets of our solar",
			"system.",
			"",
			"During the battle, alien spies managed",
			"to destroy our colonies of Uranus and",
			"Neptune, using armoured space station",
			"called DEATH STAR.",
			"",
			"We must act fast to stop the aliens from",
			"destroying all of our homeland!"
		]

		# start scrolling from the bottom of the screen
		self.y = Config.getScreenSize()[1]
		self.scrollSpeed = 50

	def renderMultilineText(self, lines, y, lineHeight, screen):
		for i, line in enumerate(lines):
			if i == 0:
				text = self.titleFont.render(line, True, self.fontColor)
			else:
				text = self.font.render(line, True, self.fontColor)

			rect = text.get_rect()
			rect.centerx = screen.get_rect().centerx
			rect.y = y + i * lineHeight
			screen.blit(text, rect)
		
	def update(self, deltaTime):
		# scroll up
		self.y -= self.scrollSpeed * deltaTime

		# detect if all text has scrolled above the screen, and go to game
		if self.y + len(self.lines) * self.lineHeight < 0:
			self.goToGameScene()

	def render(self, screen):
		screen.fill((0,0,0))

		# render bg stars
		for star in self.bgStars:
			position = map(int, star)
			randomVal = random.randrange(150, 255)
			color = (randomVal,randomVal,randomVal)
			pygame.gfxdraw.pixel(screen, position[0], position[1], (randomVal,randomVal,randomVal))
		
		self.renderMultilineText(self.lines, self.y, self.lineHeight, screen)

	# proceed to game scene - called by a menu
	def goToGameScene(self):
		pygame.mixer.music.fadeout(500)
		self.manager.goTo(GameScene())

	def handleEvents(self, events, keys):
		for event in events:
			# press any key to skip
			if event.type == pygame.KEYDOWN:
				self.goToGameScene()