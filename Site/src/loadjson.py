from collections import namedtuple

def loadjson(data):
    keys = list(map(lambda x: "id" if x == "_id" else \
        x.replace("-", "_"), data.keys()))

    return namedtuple('Struct', keys)(*data.values())