import uuid


class Entity():

    def __init__(self, position, rotation=(0, 0), health=0, max_health=0):
        self.position = position
        self.rotation = rotation
        self.health = 0
        self.max_health = 0
        self.alive = 0
        self.entity_id = str(uuid.uuid4())

    def on_update(self, dt):
        self.alive += dt

    def on_draw(self):
        pass
