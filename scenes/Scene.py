class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self, deltaTime):
        raise NotImplementedError

    def handleEvents(self, events, keys):
        raise NotImplementedError