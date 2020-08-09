import json

def load_source():
    # 读取 source.json 并解析
    source = json.load(open('sojrce.json'))
    return {'resource': source['resource'], 'block': source['block'], 'sound': source['sound']}

