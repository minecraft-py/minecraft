from json import load
from os import listdir, path

method = dict()

def get_recipes():
    recipes_path = path.abspath(path.join(path.dirname(__file__), '..', 'data', 'recipes'))
    for f in listdir(recipes_path):
        data = load(open(path.join(recipes_path, f), encoding='utf-8'))
        yield data

def match_recipe(data):
    for recipe in get_recipes():
        for name, func in method.items():
            if name == recipe['type']:
                print('match', data)
                return func(recipe, data)
    return False

def register_recipe_type(name, func):
    global method
    method.setdefault(name, func)

def crafting_shapeless(recipe, data):
    ingredients = recipe['ingredients']
    match = 0
    for i in data:
        for j in ingredients:
            if j['item'] == i:
                match += 1
    if match == len(ingredients):
        return recipe['result']
    else:
        return False

register_recipe_type('minecraft:crafting_shapeless', crafting_shapeless)
