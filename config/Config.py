import pygame

class Config():
	# display
	screenWidth = 0
	screenHeight = 0
	screenMode = 4
	flags = pygame.DOUBLEBUF | pygame.HWSURFACE # | pygame.FULLSCREEN
	fullscreen = True

	caption = "Planet Wars"
	
	bgMusic = "sound/bg.ogg"
	fps = 40

	savedGamesDB = "saved_games.db"
	
	@classmethod
	def getScreenFlags(cls):
		flags = cls.flags
		if cls.fullscreen:
			flags |= pygame.FULLSCREEN
		return flags