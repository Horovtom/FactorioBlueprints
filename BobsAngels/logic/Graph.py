from graphviz import Digraph

from logic.Recipe import Recipe
from logic.Resource import Resource
from logic.helpers import warning, convert_name


class Graph:
    def __init__(self, recipes: dict):
        self.recipes_json: dict = recipes
        self.resources: dict = {}
        self.resources_name_map: dict = {}
        self.recipes: dict = {}
        self.construct()

    def check_integrity(self):
        # TODO: Check if there are no two recipes that have the same inputs/outputs/speed.
        pass

    def get_resource_from_name(self, resource_human_name: str) -> Resource:
        """
        Returns an instance of Resource object for the speciied human name. If this Resource was not registered yet, it
        creates a new instance and adds it to the resources list automatically
        :return: Resource object
        """

        resource_converted_name = convert_name(resource_human_name)
        if resource_converted_name not in self.resources:
            # Add a new one to the list
            self.resources[resource_converted_name] = Resource(resource_human_name, resource_converted_name)
            self.resources_name_map[resource_human_name] = resource_converted_name

        return self.resources[resource_converted_name]

    def construct(self):
        def add_resources_to_recipe(r_dict: dict, r_obj: Recipe, do_input: bool):
            io = "inputs" if do_input else "outputs"
            for r in r_dict[io]:
                resource = self.get_resource_from_name(r["resource"])
                amount = float(r["amount"])
                if do_input:
                    r_obj.add_input_resource(resource, amount)
                else:
                    r_obj.add_output_resource(resource, amount)

        for recipe_name in self.recipes_json.keys():
            recipe_dict = self.recipes_json[recipe_name]
            converted_recipe_name = convert_name(recipe_name)

            # Sanity check
            if converted_recipe_name in self.recipes.keys():
                warning("Recipe: {} is actually twice in the input file. "
                        "The other has name: {}".format(recipe_name, self.recipes[converted_recipe_name].name))
                continue

            recipe_obj = Recipe(recipe_name, converted_recipe_name, recipe_dict["time"], recipe_dict["building"])

            add_resources_to_recipe(recipe_dict, recipe_obj, do_input=True)
            add_resources_to_recipe(recipe_dict, recipe_obj, do_input=False)

            self.recipes[converted_recipe_name] = recipe_obj

    def get_resources_list(self):
        res = list(self.resources_name_map.keys())
        res.sort()
        return res

    def get_dot(self, compress_water=True):
        """
        Returns dot object with the whole graph
        """

        dot = Digraph(comment="Recipes graph")
        for resource in self.resources.values():
            resource.add_to_dot(dot, compress_water)
        for recipe in self.recipes.values():
            recipe.add_to_dot(dot, compress_water)
        return dot

    def get_dot_with_filter(self, resource_human: str, depth: int, direction_str: str, compress_water: bool) -> str:
        dot = Digraph(comment="Recipes graph with filter")
        direction = 1 if direction_str == "UP" else -1 if direction_str == "DOWN" else 0

        def draw_recursive_down(resource, curr_depth, added=None):
            if added is None:
                added = []
            if curr_depth > depth:
                return

            if compress_water and resource.is_water():
                return

            for recipe in resource.ingredient_of:
                if recipe not in added:
                    recipe.add_to_dot(dot, compress_water)
                    added.append(recipe)

                for i in recipe.get_input_resources():
                    if i not in added:
                        i.add_to_dot(dot, compress_water)
                        added.append(i)

                for o in recipe.get_output_resources():
                    if o not in added:
                        o.add_to_dot(dot, compress_water)
                        added.append(o)
                    draw_recursive_down(o, curr_depth + 1, added)

        def draw_recursive_up(resource, curr_depth, added=None):
            if added is None:
                added = []
            if curr_depth > depth:
                return

            if compress_water and resource.is_water():
                return

            for recipe in resource.created_by:
                if recipe not in added:
                    recipe.add_to_dot(dot, compress_water)
                    added.append(recipe)

                for o in recipe.get_output_resources():
                    if o not in added:
                        o.add_to_dot(dot, compress_water)
                        added.append(o)
                for i in recipe.get_input_resources():
                    if i not in added:
                        i.add_to_dot(dot, compress_water)
                        added.append(i)
                    draw_recursive_up(i, curr_depth + 1, added)

        res = self.resources[self.resources_name_map[resource_human]]
        res.add_to_dot(dot, compress_water)
        if direction >= 0:
            draw_recursive_up(res, 0)
        if direction <= 0:
            draw_recursive_down(res, 0)
        return dot
