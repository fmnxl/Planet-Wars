class SceneMananger(object):
    def __init__(self, initialScene):
        self.go_to(initialScene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self