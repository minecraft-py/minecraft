import uuid


class Entity(object):

    def __init__(self):
        pass

    def draw(self):
        pass


class EntityGroup(object):

    def __init__(self):
        self.entity = {}

    def add(self, entity):
        id_ = str(uuid.uuid4())
        self.entity[id_] = entity
        return id_
