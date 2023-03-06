import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from recipe_scrapers import scrape_me
import re
import stanza

nlp = stanza.Pipeline(lang="en", processors='tokenize,pos', verbose=False)
global all_ingredients
all_ingredients = []


# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n" + "Step Ingredients: " + str(self.ingredients)

class ingredient:
    def __init__(self, ingredient):
        self.ingredient_text = ingredient
        my_regex = my_regex = "\s\(.*?\)"
        new_str = re.sub(my_regex, "", self.ingredient_text)
        temp = new_str.split()
        
        self.quantity = temp[0]
        if temp[0].isnumeric():
            self.quantity = int(self.quantity)
        self.unit = temp[1]
        self.food_item = ""

    def __str__(self):
        return "Ingredient Text: " + str(self.ingredient_text) + "\n" + "Food Item: " + self.food_item + "\n" + "Quanity: " + str(self.quantity) + " " + str(self.unit) + "\n"

def buildIngredient(ingredient):
    #print("Ingredient Text: " + ingredient.ingredient_text)
    my_regex = my_regex = "\s\(.*?\)"
    new_str = re.sub(my_regex, "", ingredient.ingredient_text)
    #print("Regexed String: " + new_str + "\n")
    doc = nlp(new_str.lower())
    i_string = ""
    
    for word in doc.sentences[0].words[2:]:
        if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
            i_string = i_string + " " + word.text
    ingredient.food_item = i_string
    return

def recipe_ingredients(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    for i in scraper.ingredients():
        i = ingredient(i)
        buildIngredient(i)
        all_ingredients.append(i)
    return

def printSteps(recipe_steps):
    for element in recipe_steps:
        print(element)

def findStepIngredients(stepClass):
    step_text = stepClass.step_text
    for i in all_ingredients:
        print(i)
        if i.food_item in step_text:
            stepClass.ingredients.append(i.food_item)
    return

def buildStepsArray(instructions):
    steps_array = []

    for c, element in enumerate(instructions):
        #print("Loading Step " + str(c+1))
        step = recipeStep(c+1, element)
        findStepIngredients(step)
        steps_array.append(step)

    return steps_array

instructions_list = scrape_me("https://www.allrecipes.com/recipe/8539106/yaki-udon/", wild_mode = True).instructions_list()
recipe = "https://www.allrecipes.com/recipe/8539106/yaki-udon/"
#recipe = "https://www.allrecipes.com/recipe/239541/chef-johns-fresh-salmon-cakes/"
new_instructions_list = []
for instruction in instructions_list:
    new_instructions_list += sent_tokenize(instruction)

recipe_ingredients(recipe)
for i in all_ingredients:
    print(i)
    
#steps = buildStepsArray(new_instructions_list)
#printSteps(steps)