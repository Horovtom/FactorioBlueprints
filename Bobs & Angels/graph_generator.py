import json

from graphviz import Digraph


# TODO: ADD FROM/TO Graph generation

def run():
    with open("recipes.json", 'r') as recipes_file:
        recipes = json.load(recipes_file)

    all_recipes = input("Do you want to filter out unused recipes? (y/n): ")
    # all_recipes = "y"
    if not (len(all_recipes) == 0 or all_recipes.lower() == "y"):
        with open("unused_recipes.json", "r") as unused_recipes_file:
            unused_recipes = json.load(unused_recipes_file)
        recipes = {**recipes, **unused_recipes}

    compress_water = input("Do you want to compress water into nodes? (y/n): ")
    compress_water = len(compress_water) == 0 or compress_water.lower() == "y"

    dot = Digraph(comment="Recipes graph :)")

    def find_all_resources():
        resources = []
        resources_in_lower = []

        def do(wh, ignore_water_compression=False):
            resource_name = wh["resource"]
            if resource_name.lower() == "water" and compress_water and not ignore_water_compression:
                return

            if resource_name.lower() not in resources_in_lower:
                resources.append(resource_name)

        for recipe in recipes.values():
            for resource in recipe["inputs"]:
                do(resource)
            for resource in recipe["outputs"]:
                do(resource, ignore_water_compression=True)

        return resources

    resources = find_all_resources()

    def get_node_name(name: str):
        return name.replace(' ', '_').replace(':', '_').lower()

    def create_recipe_nodes():
        for recipe_name in recipes.keys():
            label = "{}\\n{}\\n{}s".format(recipe_name, recipes[recipe_name]["building"], recipes[recipe_name]["time"])
            if len(list(filter(lambda x: x["resource"].lower() == "water",
                               recipes[recipe_name]["inputs"]))) > 0 and compress_water:
                label += "\\n+Water"
            dot.node(get_node_name(recipe_name), label=label, shape="box")

    def create_resource_nodes():
        for resource in resources:
            dot.node(get_node_name(resource), label=resource, shape="ellipse")

    create_recipe_nodes()
    create_resource_nodes()

    def create_recipe_outgoing_edges():
        for recipe_name in recipes.keys():
            outputs = recipes[recipe_name]["outputs"]
            craft_time = recipes[recipe_name]["time"]
            for output in outputs:
                am = output["amount"] / craft_time
                if am.is_integer():
                    label = "{}x\\n{}/s".format(output["amount"], int(am))
                else:
                    label = "{}x\\n{:.2f}/s".format(output["amount"], am)
                dot.edge(get_node_name(recipe_name), get_node_name(output["resource"]), label=label)

    def create_recipe_incoming_edges():
        for recipe_name in recipes.keys():
            inputs = recipes[recipe_name]["inputs"]
            craft_time = recipes[recipe_name]["time"]
            for input in inputs:
                if get_node_name(input["resource"]) == "water" and compress_water:
                    continue

                am = input["amount"] / craft_time
                if am.is_integer():
                    label = "{}x\\n{}/s".format(input["amount"], int(am))
                else:
                    label = "{}x\\n{:.2f}/s".format(input["amount"], am)
                dot.edge(get_node_name(input["resource"]), get_node_name(recipe_name), label=label)

    create_recipe_outgoing_edges()
    create_recipe_incoming_edges()

    dot.render("test", view=True)


if __name__ == "__main__":
    run()
