class Entity(object):

    def __init__(self):
        pass

    def draw(self):
        pass


class EntityGroup(object):

    def __init__(self):
        self.entity = []

    def add(self, entity):
        self.entity.append(entity)
