class Level(object):
    def __init__(self):
        pass

    def render(self, screen, camera):
        raise NotImplementedError

    def update(self, deltaTime):
        raise NotImplementedError

    def handleEvents(self, events, keys):
        raise NotImplementedError