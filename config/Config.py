import pygame, sys, os

class Config():
	# environment variable
	development = False
	env = "DEVELOPMENT" if development else "PRODUCTION"
	
	# display
	screenWidth = 0
	screenHeight = 0
	screenMode = 4
	flags = pygame.DOUBLEBUF | pygame.HWSURFACE # | pygame.FULLSCREEN
	fullscreen = True

	caption = "Planet Wars"
	
	bgMusic = "sound/bg.ogg"
	savedGamesDB = "saved_games.db"
	ethnocentric = "font/ethnocentric.ttf"
	neuropol = "font/neuropol.ttf"
	fps = 40


	@classmethod
	def getFile(cls, filePath):
		if cls.env == "PRODUCTION":
			return os.path.join(os.path.dirname(sys.executable), filePath)
		else:
			return filePath


	@classmethod
	def getScreenFlags(cls):
		flags = cls.flags
		if cls.fullscreen:
			flags |= pygame.FULLSCREEN
		return flags