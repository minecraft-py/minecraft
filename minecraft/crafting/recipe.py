from json import load
from os import listdir, path

def get_recipes():
    recipes_path = path.abspath(path.join(path.dirname(__file__), '..', 'data', 'recipes'))
    for f in listdir(recipes_path):
        data = load(open(path.join(recipes_path, f), encoding='utf-8'))
        yield data

def match_recipe(data):
    for recipe in get_recipes():
        if recipe['type'] == 'crafting_shaped':
            pass
        elif recipe['type'] == 'crafting_shapeless':
            ingredients = recipe['ingredients']
            match = 0
            for i in data:
                for j in ingredients:
                    if j['item'] == i:
                        match += 1
            else:
                if match == len(ingredients):
                    return recipe['result']
    else:
        return False
