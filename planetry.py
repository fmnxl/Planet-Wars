import sys, pygame
from pygame.locals import *
from config.Config import *
from scenes.Scene import *
from models.SceneManager import *
from scenes.TitleScene import TitleScene
from scenes.GameScene import GameScene

pygame.init()
modes = pygame.display.list_modes(32)
size = Config.screenWidth, Config.screenHeight = modes[4]
flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
screen = pygame.display.set_mode(size, flags)
pygame.display.set_caption('Rocketry')
clock = pygame.time.Clock()

pygame.mouse.set_visible(True)

manager = SceneMananger(TitleScene())

pygame.mixer.init()
pygame.mixer.set_num_channels(8)
pygame.mixer.music.load("sound/bg.ogg")
pygame.mixer.music.play(-1)

def main():
	while True:
		clock.tick(40)
		deltaTime = clock.get_time() / 1000.0

		events = pygame.event.get()
		for event in events:
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_p):
				pygame.quit()
				sys.exit()

		keys = pygame.key.get_pressed()

		manager.scene.handleEvents(events, keys)
		manager.scene.update(deltaTime)
		manager.scene.render(screen)
		pygame.display.flip()

if __name__ == "__main__":
    main()
	