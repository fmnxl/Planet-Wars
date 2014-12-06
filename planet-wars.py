import sys, pygame
from pygame.locals import *
from config.Config import *
from scenes.Scene import *
from models.SceneManager import *
from scenes.TitleScene import TitleScene
from scenes.GameScene import GameScene

pygame.init()
modes = pygame.display.list_modes(32)
size = Config.screenWidth, Config.screenHeight = modes[Config.screenMode]
screen = pygame.display.set_mode(size, Config.getScreenFlags())
pygame.display.set_caption(Config.caption)
clock = pygame.time.Clock()

pygame.mouse.set_visible(True)

manager = SceneMananger(TitleScene())

# bg music
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
pygame.mixer.music.load(Config.getFile(Config.bgMusic))
pygame.mixer.music.play(-1)

def main():
	while True:
		clock.tick(Config.fps)
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
	