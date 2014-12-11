import sys, pygame
from config.Config import Config
from scenes.Scene import Scene
from models.SceneManager import SceneMananger
from scenes.TitleScene import TitleScene
from scenes.GameScene import GameScene

pygame.init()
Config.load()
modes = pygame.display.list_modes(32)
size = modes[Config.screenMode]
screen = pygame.display.set_mode(size, Config.getScreenFlags())
pygame.display.set_caption(Config.caption)
clock = pygame.time.Clock()

pygame.mouse.set_visible(True)

manager = SceneMananger(TitleScene())

# bg music
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

def main():
	while True:
		clock.tick(Config.fps)
		deltaTime = clock.get_time() / 1000.0 # in seconds

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		keys = pygame.key.get_pressed()

		manager.scene.handleEvents(events, keys)
		manager.scene.update(deltaTime)
		manager.scene.render(screen)
		pygame.display.flip()

if __name__ == "__main__":
    main()
	