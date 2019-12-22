import json

with open("resources/recipes.json", 'r') as recipes_file:
    recipes = json.load(recipes_file)

while True:
    print("===== NEW RECIPE =====")
    recipe_name = input("Recipe name: ")

    if recipe_name in recipes:
        print("ERROR: There is already such recipe in the recipes list!")
        continue
    elif len(recipe_name) == 0:
        i = input("ERROR: No recipe name entered. Do you want to stop? (y/n) ")
        if len(i) == 0 or i.lower() == "y":
            break
        else:
            continue

    def load_resources_until_stopped():
        ret = []
        while True:
            res_name = input("\tEnter resource name: ")
            if len(res_name) == 1 or len(res_name) == 0:
                break
            res_amount = float(input("\tHow many of {}? ".format(res_name)))
            ret.append({"resource": res_name, "amount": res_amount})
        return ret


    print("Enter inputs as asked, one-letter name of input to stop:")

    inputs = load_resources_until_stopped()

    print("Enter outputs as asked, one-letter name of output to stop:")
    outputs = load_resources_until_stopped()

    time = float(input("Enter recipe craft time (in seconds): "))
    building = input("Enter recipe crafting building: ")

    rec_dict = {
        "inputs": inputs,
        "outputs": outputs,
        "time": time,
        "building": building
    }

    recipes[recipe_name] = rec_dict

    with open("resources/recipes.json", "w") as recipes_file:
        json.dump(recipes, recipes_file)

    i = input("\n\nAnother one? (y/n) ")
    if not (len(i) == 0 or i.lower() == "y"):
        break
