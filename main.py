# main file
from recipe_scrapers import scrape_me

# to get ingredients for each step, 




# step class
class recipeStep:
    def __init__(self, step_num, step_text, step_ingredients):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = step_ingredients
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text
        
#ingredients will be a field of recipe step, with step 0 holding all of the ingredients
class ingredient:
    def __init__(self, ingredient):
        self.ingredient = ingredient
    
def recipe_scraper(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    return scraper.ingredients()


    for c, element in enumerate(instructions):
        step = recipeStep(c, element)
        steps_array.append(step)

    return steps_array

def recipe_ingredients(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    return scraper.ingredients()

def printHelp():
    print("Here is a list of possible ways you can interact with me\n")
    print("- Go to next or previous step\n")
    print("- Ask questions about the current step\n")
    print("- Ask about the ingredients or utensils\n")
    print("If you even need a refresher on these simply type 'help' in the chat")

def printSteps(recipe_steps):
    for element in recipe_steps:
        print(element)

def printIngredients(ingredients):
    for i in ingredients:
        #i = ingredient(i)
        print(i)


if __name__ == "__main__":
    print("Welcome to Recipe Extravaganza!\n")
    printHelp()
    recipe = input("Please give me a link to a recipe:\n")
    print("Holy Guacamole! That sounds yummy. To start you off here are the list of ingredients you will need:\n")
    #print(recipe_scraper(recipe))
    printIngredients(recipe_ingredients(recipe))


    '''
    while True:
        query = input("")
        #chatbot exti
        if query in exit_conditions:
            break
        #chatbot help
        if query in help_conditions:
            printHelp()
        if query == "next":
            if recipe_pointer >= len(recipe_steps) - 1:
                print("We've reached the end of our recipe")
            else:
                recipe_pointer += 1
                print(recipe_steps[recipe_pointer])
        elif query == "back":
            if recipe_pointer == 0:
                print("Sorry we can't go back a step, we are at Step #0")
            else:
                recipe_pointer -= 1
                print(recipe_steps[recipe_pointer])
    '''


