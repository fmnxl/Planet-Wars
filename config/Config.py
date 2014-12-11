import pygame, sys, os, shelve

class Config():
	

	# environment variable
	development = True
	env = "DEVELOPMENT" if development else "PRODUCTION"
	
	# display
	screenMode = 0
	flags = 0 # pygame.DOUBLEBUF | pygame.HWSURFACE # | pygame.FULLSCREEN
	fullscreen = True

	caption = "Planet Wars"
	
	titleBgMusic = "sound/imperial-march.ogg"
	introBgMusic = "sound/title.ogg"
	savedGamesDB = "saved_games.db"
	ethnocentric = "font/ethnocentric.ttf"
	neuropol = "font/neuropol.ttf"
	fps = 40


	# for PyInstaller
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

	@classmethod
	def getScreenSize(cls):
		modes = pygame.display.list_modes(32)
		return modes[cls.screenMode]

	@classmethod
	def load(cls):
		db = shelve.open("config.db")
		
		# if doesn't exist, then initialise
		try:
			config = db["config"]
		except:
			config = {}
			config["fullscreen"] = cls.fullscreen
			config["screenMode"] = cls.screenMode
			db["config"] = config

		cls.fullscreen = config["fullscreen"]
		cls.screenMode = config["screenMode"]
		db.close()


	@classmethod
	def save(cls):
		db = shelve.open("config.db")
		config = db["config"]
		config["fullscreen"] = cls.fullscreen
		config["screenMode"] = cls.screenMode
		db["config"] = config
		db.close()