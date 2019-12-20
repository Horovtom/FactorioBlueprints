from logic import Recipe


class Resource:
    def __init__(self, human_name, converted_name):
        self.human_name = human_name
        self.converted_name = converted_name

        self.created_by = []
        self.ingredient_of = []

    def add_as_result(self, recipe: Recipe):
        self.created_by.append(recipe)

    def add_as_ingredient(self, recipe: Recipe):
        self.ingredient_of.append(recipe)

    def add_to_dot(self, dot_obj, compress_water=True):
        if compress_water and self.human_name.lower() == "water":
            return

        dot_obj.node(self.converted_name, label=self.human_name, shape="ellipse", style="filled", fillcolor="crimson")
