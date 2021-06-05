import json

class NBT(object):

    def __init__(self, data={}):
        self._nbt = dict()
        self.set_values(data)

    def load_dict(self, d):
        for k, v in d.items():
            self.set_value(k, v)
        else:
            return True

    def load_json(self, s):
        value = json.loads(s)
        if isinstance(value, dict):
            for k,v in value.items():
                self.set_value(k, v)
            else:
                return True
        else:
            return False

    def set_value(self, key, value):
        if isinstance(key, str):
            # 只允许字符串形式的键名
            if isinstance(value, (bool, int, float, str, list, dict)) or (value is None):
                # python 的内建类型大多都可以转化到 json
                self._nbt[key] = value
                return True
            else:
                return False
        else:
            return False

    def set_values(self, data):
        for k, v in data.items():
            self.set_value(k, v)

    def get_dict(self):
        return self._nbt

    def get_json(self):
        return json.dumps(self._nbt)
