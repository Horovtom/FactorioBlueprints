import json

# TODO: ADD FROM/TO Graph generation
from Graph import Graph


def run():
    with open("recipes.json", 'r') as recipes_file:
        recipes = json.load(recipes_file)

    g = Graph(recipes)

    compress_water = input("Do you want to compress water into nodes? (y/n): ")
    compress_water = len(compress_water) == 0 or compress_water.lower() == "y"

    dot = g.get_dot(compress_water)

    dot.render("testaa", view=True)


if __name__ == "__main__":
    run()
