class ResourcePack():

    def __init__(self, name):
        self.name = name
        self.lang = dict()

    def set_lang(self, lang):
        # 成功则返回 True
        # 否则返回 False
        pass

    def get_translation(self, name):
        return self.lang.get(name, name)

    def get_pack_info(self):
        # 返回一个 (pack.json, pack.png) 
        pass

    def get_resource(self, path):
        # path 为用 '/' 分隔的路径名
        # lang/*     - *.json(不建议)
        # sounds/*   - *.ogg
        # textures/* - *.png
        pass
