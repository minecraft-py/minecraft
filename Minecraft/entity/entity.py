class Entity(object):

    def __init__(self, position, rotation, health=0, max_health=0):
        # 普通的实体
        self.position = position
        self.rotation = rotation
        self.max_health = health
        if health > self.max_health:
            self.health = self.max_health
        else:
            self.health = health
        self.id = None

    def event_handle(self, *args, **kwargs):
        pass


class BlockEntity(Entity):

    def __init__(self, world, position):
        # 方块实体
        super(BlockEntity, self).__init__(self, position, rotation=(0, 0))
        self.world = world


class EntityGroup(object):

    def __init__(self):
        # 实体组
        self.entity = []
        self.last_id = 0

    def add(self, entity):
        self.last_id += 1
        self.entity[self.last_id] = entity
        self.entity[self.last_id].id = self.last_id

    def remove(self, entity_id):
        del self.entity[entity_id]
