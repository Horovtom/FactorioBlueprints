from logic import Resource
from logic.helpers import format_number


class Recipe:
    def __init__(self, human_name: str, converted_name: str, recipe_speed: float, recipe_building: str):
        self.human_name = human_name
        self.converted_name = converted_name
        self.input_resources: dict = {}
        self.output_resources: dict = {}
        self.time: float = recipe_speed
        self.building = recipe_building

    def add_input_resource(self, resource: Resource, amount):
        if amount.is_integer():
            amount = int(amount)
        self.input_resources[resource.converted_name] = (resource, amount)
        resource.add_as_ingredient(self)

    def add_output_resource(self, resource: Resource, amount):
        if amount.is_integer():
            amount = int(amount)
        self.output_resources[resource.converted_name] = (resource, amount)
        resource.add_as_result(self)

    def get_input_resources(self):
        return [x[0] for x in self.input_resources.values()]

    def get_output_resources(self):
        return [x[0] for x in self.output_resources.values()]

    def add_to_dot(self, dot_obj, compress_water=True):

        label = "{}\\n{}\\n{}s".format(self.human_name, self.building, format_number(self.time))
        if compress_water and any(x.is_water() for x in self.get_input_resources()):
            label += "\\n+Water"

        dot_obj.node(self.converted_name, label=label, shape="box", style="filled", fillcolor="skyblue")

        # Add edges:
        for resource, amount in self.input_resources.values():
            # Water compression
            if compress_water and resource.converted_name == "water":
                continue

            per_sec = format_number(amount / self.time)
            label = "{}x\\n{}/s".format(amount, per_sec)
            dot_obj.edge(resource.converted_name, self.converted_name, label=label)

        for resource, amount in self.output_resources.values():
            per_sec = format_number(amount / self.time)
            label = "{}x\\n{}/s".format(amount, per_sec)
            dot_obj.edge(self.converted_name, resource.converted_name, label=label)
