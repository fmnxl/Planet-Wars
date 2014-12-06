class SceneMananger(object):
    def __init__(self, initialScene):
        self.goTo(initialScene)

    def goTo(self, scene):
        self.scene = scene
        self.scene.manager = self