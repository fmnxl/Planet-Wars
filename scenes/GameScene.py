import pygame, math, random, pygame.gfxdraw, sys
from pygame.locals import *
from lib.euclid import *
from config.Config import *
from scenes.Scene import *
from scenes.GameOverScene import GameOverScene
from models.Alien import *
from models.Camera import *
from models.Planet import *
from models.Moon import *
from models.Asteroid import *
from models.Probe import *
from models.Sun import *

from models.LevelManager import *
from scenes.levels.Level1 import *
from models.SavedGame import *



class GameScene(Scene):
	def __init__(self, savedGame = None):
		super(GameScene, self).__init__()

		self.level = 1
		self.paused = False

		self.camera = Camera(Vector2(Config.screenWidth, Config.screenHeight))
		
		# setup solar system
		self.sun = Sun()
		#					size	mass	dist	year	colour						center
		mercury = Planet("Mercury",	0.383, 	3200, 	57.0, 	900, 	"img/planets/mercury.png", 	self.sun, math.radians(random.randrange(0, 359)))
		venus 	= Planet("Venus",	0.95, 	3200, 	108.0, 	2000, 	"img/planets/venus.png", 	self.sun, math.radians(random.randrange(0, 359)))
		earth 	= Planet("Earth",	1.0, 	3200, 	150.0, 	3650, 	"img/planets/earth.png", 	self.sun, math.radians(random.randrange(0, 359)))
		mars 	= Planet("Mars",	0.532, 	3200, 	227.0, 	7000, 	"img/planets/mars.png", 	self.sun, math.radians(random.randrange(0, 359)))
		jupiter = Planet("Jupiter",	11.2, 	12000, 	778.0, 	36000, 	"img/planets/jupiter.png", 	self.sun, math.radians(random.randrange(0, 359)))
		saturn 	= Planet("Saturn",	9.45, 	5000, 	1426.0, 80000, 	"img/planets/saturn.png", 	self.sun, math.radians(random.randrange(0, 359)))

		# moons
		#earth
		moon = Moon(		0.5, 	100, 	15.0, 	80, 	"img/planets/moon.png", 	earth, math.radians(random.randrange(0, 359)))
		earth.moons.append(moon)

		#mars
		phobos = Moon(		0.2, 	100, 	5.0, 	30, 	"img/planets/moon.png", 	mars, math.radians(random.randrange(0, 359)))
		deimos = Moon(		0.2, 	100, 	8.0, 	40, 	"img/planets/moon.png", 	mars, math.radians(random.randrange(0, 359)))
		mars.moons.append(phobos)
		mars.moons.append(deimos)

		#jupiter
		europa 		= Moon(		0.2, 	100, 	25.0, 	60, 	"img/planets/moon.png", 	jupiter, math.radians(random.randrange(0, 359)))
		io 			= Moon(		0.2, 	100, 	20.0, 	80, 	"img/planets/moon.png", 	jupiter, math.radians(random.randrange(0, 359)))
		ganymede 	= Moon(		0.2, 	100, 	25.0, 	100, 	"img/planets/moon.png", 	jupiter, math.radians(random.randrange(0, 359)))
		callisto 	= Moon(		0.2, 	100, 	30.0, 	120, 	"img/planets/moon.png", 	jupiter, math.radians(random.randrange(0, 359)))
		jupiter.moons.append(europa)
		jupiter.moons.append(io)
		jupiter.moons.append(ganymede)
		jupiter.moons.append(callisto)

		self.planets = [mercury, venus, earth, mars, jupiter, saturn]


		# asteroids
		self.asteroids = []
		for i in range(0, 500):
			size = random.randrange(4, 15) / 10.0
			self.asteroids.append(Asteroid(	size, 	1, 	random.randrange(400,600), 	random.randrange(100, 300), (100, 100, 100), 	self.sun, math.radians(random.randrange(0, 359))))

		# asteroids
		# for i in range(0, 80):
		# 	size = random.randrange(1, 3) / 10.0
		# 	self.planets.append(Asteroid(	size, 	1, 	random.randrange(10,15), 	random.randrange(100, 300), (100, 100, 100), 	saturn, math.radians(random.randrange(0, 359))))

		self.probe = Probe(earth.position + Vector2(20,0), Vector2(0,0))
		self.aliens = []

		earth.setZone(8, 10, 10, self.probe)

		self.levelManager = LevelManager(Level1(), self.planets, self.probe, self.aliens)


		self.bgStars = []
		for i in range(0, 200):
			self.bgStars.append(Vector2(random.randrange(-Config.screenWidth/2, Config.screenWidth/2), random.randrange(-Config.screenHeight/2, Config.screenHeight/2)))

		# gui
		self.currentSelection = 0
		self.selectionsRects = []

		self.guiImage = pygame.image.load("img/gui.png").convert_alpha()
		self.guiRect = self.guiImage.get_rect()
		self.selectSound = pygame.mixer.Sound("sound/select.ogg")

		if savedGame is not None:
			savedGame.loadTo(self.planets, self.probe, self.aliens)
			self.paused = True



	def update(self, deltaTime):

		if self.paused:
			return

		# update
		for planet in self.planets:
			planet.update(deltaTime)

		for asteroid in self.asteroids:
			asteroid.update(deltaTime)

		self.probe.update(deltaTime)

		for alien in self.aliens:
			alien.update(deltaTime)

		self.camera.update(deltaTime, self.probe)

		# Game logic (Level-invariant)

		# sun
		self.sun.attract(self.probe)
		self.sun.attractMulti(self.aliens)
		if self.sun.checkCollision(self.probe):
			self.manager.go_to(GameOverScene(self.levelManager.lastCheckpoint, "YOU CRASHED INTO THE SUN"))
			return

		# planets
		for planet in self.planets:
			planet.attract(self.probe)
			planet.attractMulti(self.aliens)
			if planet.checkCollision(self.probe):
				self.manager.go_to(GameOverScene(self.levelManager.lastCheckpoint, "YOU CRASHED"))
				return

		# probe
		self.probe.checkBulletHit(self.aliens, self.camera)
		if self.probe.shouldDie():
			self.manager.go_to(GameOverScene(self.levelManager.lastCheckpoint))
			return
		
		for alien in self.aliens:
			alien.checkBulletHit(self.probe, self.camera)
			if alien.health <= 0:
				self.aliens.remove(alien)

		self.levelManager.level.update(deltaTime)


	def render(self, screen):
		screen.fill((0,0,0))

		# random stars
		for star in self.bgStars:
			position = map(int, self.camera.convertCoordinatesParallax(star, 0.3))
			randomVal = random.randrange(100, 255)
			color = (randomVal,randomVal,randomVal)
			pygame.gfxdraw.pixel(screen, position[0], position[1], (randomVal,randomVal,randomVal))

		# sun
		self.sun.blit(screen, self.camera)

		# planets
		for planet in self.planets:
			planet.blit(screen, self.camera)

		# asteroids
		for asteroid in self.asteroids:
			asteroid.blit(screen, self.camera)

		# probe
		self.probe.blit(screen, self.camera)

		# aliens
		for alien in self.aliens:
			alien.blit(screen, self.camera)

		# GUI
		if self.paused:
			self.showPauseMenu(screen)

		self.renderObjectDesc(screen)
		self.renderNearestPlanet(screen, self.camera)

		# level specific
		self.levelManager.level.render(screen, self.camera)

	def renderNearestPlanet(self, screen, camera):
		# GUI - Object desc
		color = (0,254,253)
		
		# heading
		guiFont = pygame.font.Font("font/neuropol.ttf", 18)
		heading = guiFont.render("Nearest Planet", True, color)
		headingRect = pygame.Rect(screen.get_rect().left + 10, screen.get_rect().bottom - 200, 400, 30)
		screen.blit(heading, (headingRect.left + 10, headingRect.top + 7))

		#border
		descRect = pygame.Rect(headingRect.left, headingRect.bottom + 10, 400, 150)
		borderRect = descRect
		borderRect.height = 2
		pygame.draw.rect(screen, color, borderRect, 0)

		# planet name
		closestPlanet = None
		closestDistanceSq = 0
		for planet in self.planets:
			distanceToPlanetSq = (camera.center - planet.position).magnitude_squared()
			if closestPlanet is None or distanceToPlanetSq < closestDistanceSq:
				closestPlanet = planet
				closestDistanceSq = distanceToPlanetSq

		font = pygame.font.Font("font/ethnocentric.ttf", 30)
		text = font.render(closestPlanet.name, True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 10))

		font = pygame.font.Font("font/neuropol.ttf", 17)

		text = font.render("Distance : " + str(int(math.sqrt(closestDistanceSq))), True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 60))

		hasHumanPresence = "Yes" if closestPlanet.zoneRadius > 0 else "No"
		text = font.render("Human Presence : " + hasHumanPresence, True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 85))

		text = font.render("Distance From Sun: " +  str(closestPlanet.distance), True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 110))

		originalImage = closestPlanet.originalImage
		zoomedImage = pygame.transform.smoothscale(originalImage, (100,100))
		probeRect = zoomedImage.get_rect()
		probeRect.topright = (descRect.right - 10, descRect.top + 10)
		screen.blit(zoomedImage, probeRect)

	def renderObjectDesc(self, screen):
		# GUI - Object desc
		color = (0,254,253)
		windowSize = Vector2(400, 150)
		
		guiFont = pygame.font.Font("font/neuropol.ttf", 18)
		heading = guiFont.render("Object description", True, color)
		headingRect = pygame.Rect(screen.get_rect().right - 10 - windowSize.x, screen.get_rect().bottom - 200, windowSize.x, 30)
		# pygame.draw.rect(screen, color, headingRect, 0)
		screen.blit(heading, (headingRect.left + 10, headingRect.top + 7))

		descRect = pygame.Rect(headingRect.left, headingRect.bottom + 10, windowSize.x, windowSize.y)
		borderRect = descRect
		borderRect.height = 2
		# pygame.draw.rect(screen, (0,0,0), descRect, 0)
		pygame.draw.rect(screen, color, borderRect, 0)

		font = pygame.font.Font("font/ethnocentric.ttf", 30)
		text = font.render("FR-71", True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 10))

		font = pygame.font.Font("font/neuropol.ttf", 17)

		text = font.render("Health : " + str(self.probe.health) + "/" + str(self.probe.maxHealth), True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 60))

		text = font.render("Fuel : " + str(round(self.probe.fuel, 1)) + "/" + str(self.probe.fuelCapacity), True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 85))

		text = font.render("Speed: " +  str(int(self.probe.speed.magnitude() * 100)) + "/" + str(self.probe.maxSpeed * 100), True, color)
		screen.blit(text, (descRect.left + 10, descRect.top + 110))

		originalImage = pygame.image.load("img/rocket4.png").convert_alpha()
		imageSize = Vector2(173, 291) * 0.5
		zoomedImage = pygame.transform.smoothscale(originalImage, map(int, (imageSize)))
		probeRect = zoomedImage.get_rect()
		probeRect.topright = (descRect.right - 10, descRect.top + 10)
		screen.blit(zoomedImage, probeRect)
	
	def showPauseMenu(self, screen):
		menuRect = pygame.Rect(0,0, 400, 400)
		menuRect.center = screen.get_rect().center

		self.selections = ["RESUME", "SAVE GAME", "MAIN MENU", "QUIT"]
		selectionsTexts = []
		selectionsRects = []

		menuFont = pygame.font.Font("font/ethnocentric.ttf", 40)
		for index, item in enumerate(self.selections):
			text = menuFont.render(item, True, (255,255,255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().centerx
			textRect.y = menuRect.top + 30 + index * 60
			selectionsTexts.append(text)
			selectionsRects.append(textRect)

		self.selectionsRects = selectionsRects

		highlightRect = selectionsRects[self.currentSelection].copy()
		highlightRect.top = selectionsRects[self.currentSelection].bottom
		highlightRect.height = 2

		pygame.draw.rect(screen, (0,254,253), highlightRect, 0)
		for i, text in enumerate(selectionsTexts):
				screen.blit(text, selectionsRects[i])

	def selectOnMenu(self):
		if self.currentSelection == 0:
			self.paused = False
		elif self.currentSelection == 1:
			savedGame = SavedGame("Saved Game", self.planets, self.probe, self.aliens)
			savedGame.save()
			self.paused = False
		elif self.currentSelection == 2:
			from scenes.TitleScene import *
			self.manager.go_to(TitleScene())
		elif self.currentSelection == 3:
			pygame.quit()
			sys.exit()

	def handleEvents(self, events, keys):
		mousePos = pygame.mouse.get_pos()

		for event in events:
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				self.paused = not self.paused

			if self.paused:
				if event.type == MOUSEBUTTONUP:
					for i, rect in enumerate(self.selectionsRects):
						if rect.collidepoint(mousePos):
							self.selectOnMenu()
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
						self.selectOnMenu()

				return

		self.probe.listenToKeyboard(keys)
		self.camera.listenToKeyboard(keys, events)	