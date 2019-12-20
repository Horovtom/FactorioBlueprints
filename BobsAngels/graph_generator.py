# TODO: ADD FROM/TO Graph generation
import json

from gui.gui import GUI
from logic.Graph import Graph

with open("resources/recipes.json", 'r') as recipes_file:
    recipes = json.load(recipes_file)

g = Graph(recipes)

a = GUI(g)
a.run()

# def run():
#     with open("resources{}recipes.json".format(os.sep), 'r') as recipes_file:
#         recipes = json.load(recipes_file)
#
#     g = Graph(recipes)
#
#     compress_water = input("Do you want to compress water into nodes? (y/n): ")
#     compress_water = len(compress_water) == 0 or compress_water.lower() == "y"
#
#     dot = g.get_dot(compress_water)
#
#     dot.render("output", view=True)
#
#
# if __name__ == "__main__":
#     run()
