from traceback import print_exc


class EntityManager():

    def __init__(self):
        self.entity = dict()

    def add_entity(self, obj):
        self.entity.setdefault(obj.entity_id, obj)

    def remove_entity(self, entity_id):
        try:
            del self.entity[entity_id]
        except:
            pass

    def get(self):
        return list(self.entity.values())

    def on_draw(self):
        try:
            for entity in self.entity.values():
                entity.on_draw()
        except:
            print_exc()

    def on_update(self, dt):
        try:
            for entity in self.entity.values():
                entity.on_update(dt)
        except:
            print_exc()
