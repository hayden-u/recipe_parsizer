# main file
from recipe_scrapers import scrape_me
#import nltk
#from nltk.tokenize import sent_tokenize, word_tokenize
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import stanza
#stanza.download('en')
nlp = stanza.Pipeline(lang='en')

# to get ingredients for each step, 

# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text
        
#ingredients will be a field of recipe step, with step 0 holding all of the ingredients
class ingredient:
    def __init__(self, ingredient):
        self.ingredient = ingredient
        temp = ingredient.split()
        self.quantity = temp[0]
        if temp[0].isnumeric():
            self.quantity = int(self.quantity)
        self.unit = temp[1]

def recipe_scraper(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    return scraper.instructions_list()

def findStepIngredients(stepClass):
    #function will find each individual ingredient in the given step
    # then populate the step class ingredient field
    text = stepClass.step_text.lower()
    document = nlp(text)
    pos_tagged = nltk.pos_tag(tokenized)
    print(pos_tagged)
    pass

def buildStepsArray(instructions):
    steps_array = []

    for c, element in enumerate(instructions):
        
        step = recipeStep(c+1, element)
        findStepIngredients(step)
        steps_array.append(step)
        break

    return steps_array

def recipe_ingredients(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    return scraper.ingredients()

def printHelp():
    print("Here is a list of possible ways you can interact with me\n")
    print("1. Next Step\n")
    print("2. Previous Step\n")
    print("3. What ingredient(s) do I need here\n")
    print("4. What material(s) do I need here?\n")
    print("5. How much of ingredient ___ do I need?\n")
    print("6. What are all of the ingredients needed for this recipe?\n")
    print("7. Any questions about timed aspects of the recipe\n")
    print("8. Does this recipe (as a whole) call for ingredient___?\n")
    #print("- Ask questions about the current step\n")
    #print("- Ask about the ingredients or utensils\n")
    #print("- Ask about the actions you need to perform\n")
    print("If you even need a refresher on these simply type 'help' in the chat")

def printSteps(recipe_steps):
    for element in recipe_steps:
        print(element)

def printIngredients(ingredients):
    for i in ingredients:
        i = ingredient(i)
        print(i.ingredient)

def runChatbot():
    print("Welcome to Recipe Extravaganza!\n")
    printHelp()
    recipe = input("Please give me a link to a recipe:\n")
    print("Holy Guacamole! That sounds yummy. To start you off here are the list of ingredients you will need:\n")
    #print(recipe_scraper(recipe))
    instructions_list = recipe_scraper(recipe)
    printIngredients(recipe_ingredients(recipe))
    #recipe_steps = buildStepsArray(instructions_list)

    exit_conditions = ["quit"]
    help_conditions = ["help"]
    recipe_pointer = 0
    
    '''
    while True:
        query = input("")
        #chatbot exti
        if query in exit_conditions:
            break
        #chatbot help
        if query in help_conditions:
            printHelp()
        if query == "1":
            if recipe_pointer >= len(recipe_steps) - 1:
                print("We've reached the end of our recipe, Bon Appetite!")
            else:
                recipe_pointer += 1
                print(recipe_steps[recipe_pointer])
        elif query == "2":
            if recipe_pointer == 0:
                print("Sorry we can't go back a step, we are at Step #0")
            else:
                recipe_pointer -= 1
                print(recipe_steps[recipe_pointer])
        elif query == "3":
            print("Sure! heres a list of what you need here:\n")
            print(recipe_steps[recipe_pointer].ingredients)

    
    '''


if __name__ == "__main__":
    print("Start of Program")
    # yaki udon
    instructions_list = recipe_scraper("https://www.allrecipes.com/recipe/8539106/yaki-udon/")
    #print(instructions_list)

    new_instructions_list = []
    for instruction in instructions_list:
        new_doc = nlp(instruction)
        new_instructions_list += new_doc.sentences()

    print(new_instructions_list)
    # recipe_steps hold our array of Step classes for navigation
    #recipe_steps = buildStepsArray(new_instructions_list)

    #printSteps(recipe_steps)
   