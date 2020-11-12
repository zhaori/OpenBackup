import json


class PyJson(object):
    def __init__(self, file):
        self.file = file
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                self.json_dict = dict(json.loads(f.read()))
        except FileNotFoundError:
            pass

    def write(self, data: dict):
        with open(self.file, 'w', encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def read(self, key):
        return self.json_dict[key]

    def upgrade(self, key, value):
        self.json_dict[key] = value
        with open(self.file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.json_dict))

# p = PyJson('setting.json')
# print(p.read('name'))
