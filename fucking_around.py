import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.symbols import nsubj, VERB
from recipe_scrapers import scrape_me
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

import stanza
import requests
import bs4
import re
import os


stop = STOP_WORDS

unnecessaryDescriptions = ['chunks', 'pieces', 'rings', 'spears', 'slice', 'slices']
descriptions = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'broken', 'chilled',
		'chopped', 'cleaned', 'coarse', 'cold', 'cooked', 'cool', 'cooled', 'cored', 'creamed', 'crisp', 'crumbled',
		'crushed', 'cubed', 'cut', 'deboned', 'deseeded', 'diced', 'dissolved', 'divided', 'drained', 'dried', 'dry',
		'fine', 'firm', 'fluid', 'fresh', 'frozen', 'grated', 'grilled', 'ground', 'halved', 'hard', 'hardened',
		'heated', 'heavy', 'juiced', 'julienned', 'jumbo', 'large', 'lean', 'light', 'lukewarm', 'marinated',
		'mashed', 'medium', 'melted', 'minced', 'near', 'opened', 'optional', 'packed', 'peeled', 'pitted', 'popped',
		'pounded', 'prepared', 'pressed', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'ripe', 'roasted',
		'roasted', 'rolled', 'rough', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'separated',
		'shredded', 'sifted', 'skinless', 'sliced', 'slight', 'slivered', 'small', 'soaked', 'soft', 'softened',
		'split', 'squeezed', 'stemmed', 'stewed', 'stiff', 'strained', 'strong', 'thawed', 'thick', 'thin', 'tied', 
		'toasted', 'torn', 'trimmed', 'wrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned', 'patted', 'raw', 'flaked', 'deveined', 'shelled', 'shucked', 'crumbs',
		'halves', 'squares', 'zest', 'peel', 'uncooked', 'butterflied', 'unwrapped', 'unbaked', 'warmed', 'lengthwise']

cooking_utensils = ['apple corker', 'apple cutter', 'baster', 'biscuit cutter', 'blow torch', 'pot', 'pan', 'bowls', 'pans', 'tong', 'skillet', 'wok', 'knife',
        'bottle opener', 'bowl', 'bread knife', 'baking sheet', 'butter curler', 'cheese knife', 'cherry pitter', 'chinois', 'cleaver',
        'colander', 'strainer', 'corkscrew', 'crab cracker', 'dough scraper', 'egg piercer', 'egg poacher', 'egg timer', 'fillet knife',
        'fish scaler', 'scale', 'flour sifter', 'food mill', 'funnel', 'garlic press', 'grater', 'ladle', 'spoon', 'spatula', 'fork',
        'lemon squeezer', 'lobster pick', 'measuring cup', 'meat grinder', 'thermometer', 'melon baller', 'mezzaluna', 'nutcracker',
        'oven mitt', 'oven glove', 'peeler', 'pepper mill', 'pizza cutter', 'potato masher', 'pot-holder', 'poultry shears', 'rolling pin', 'scissors',
        'tongs', 'whisk', 'wooden spoon', 'zester', 'cutting board', 'waffle iron', 'oven', 'microwave', 'blender', 'stove', 'aluminum foil', 'foil', 'baking dish', 
        'plastic wrap', 'wrap', 'dish', 'board', 'cutting board']

# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
        self.actions = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n" + "Step Ingredients: " + str(self.ingredients) + "\n" + "Step Mats: " + str(self.materials) + "\n" + "Step Actions: " + str(self.actions)

class ingredient:
    def __init__(self, ingredient):
        self.ingredient_text = ingredient
        my_regex = "\s\(.*?\)"
        new_str = re.sub(my_regex, "", self.ingredient_text)
        temp = new_str.split()
        
        self.quantity = temp[0]
        if temp[0].isnumeric():
            self.quantity = int(self.quantity)
        self.unit = temp[1]
        self.food_item = ""

    def __str__(self):
        return "Ingredient Text: " + str(self.ingredient_text) + "\n" + "Food Item: " + self.food_item + "\n" + "Quanity: " + str(self.quantity) + " " + str(self.unit) + "\n"



# def buildIngredient(ingredient):
#     #print("Ingredient Text: " + ingredient.ingredient_text)
#     my_regex = my_regex = "\s\(.*?\)"
#     new_str = re.sub(my_regex, "", ingredient.ingredient_text)
#     #print("Regexed String: " + new_str + "\n")
#     tokens = nltk.word_tokenize(new_str.lower())
#     tagged = nltk.pos_tag(tokens)
#     #print(tagged)
#     i_string = ""
    
#     for word in tagged[2:]:
#         if word[1] == "NN" or word[1] == "NNS" or word[1] == "NNP":
#             i_string = i_string + " " + word[0]
#     ingredient.food_item = i_string
#     return

def buildIngredient(ingredient):
    #print("Ingredient Text: " + ingredient.ingredient_text)
    my_regex = my_regex = "\s\(.*?\)"
    new_str = re.sub(my_regex, "", ingredient.ingredient_text)
    #print("Regexed String: " + new_str + "\n")

    doc = nlp2(new_str.lower())
    i_string = ""
    
    for word in doc.sentences[0].words[2:]:
        if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
            i_string = i_string + " " + word.text
    ingredient.food_item = i_string
    return

def recipe_ingredients(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    global recipe_title
    recipe_title = scraper.title()
    global all_ingredients
    all_ingredients = []
    for i in scraper.ingredients():
        i = ingredient(i)
        buildIngredient(i)
        all_ingredients.append(i)
    return

def printTags(about_doc):
    for token in about_doc:
        print(
            f"""
            TOKEN: {str(token)}
            =====
            TAG: {str(token.tag_):10} POS: {token.pos_}
            EXPLANATION: {spacy.explain(token.tag_)}"""
        )

def printDeprel(about_doc):
    for token in about_doc:
        print(
            f"""
            TOKEN: {token.text}
            =====
            {token.tag_ = }
            {token.head.text = }
            {token.dep_ = }"""
        )

def buildFullFoodList():
    global food_list
    food_list = []
    for ing in all_ingredients:
        for word in ing.food_item.split():
            if word not in unnecessaryDescriptions:
                food_list.append(word)

    food_list = " ".join(food_list)
    return

def checkList(text, list):
    is_present = False
    for element in list:
        if text in element:
            is_present = True
    return is_present

def setStepFields(step):

    noun_stop_words = ["heat", "temperature", "cool", "garnish", "lengthwise", "degrees"]
    ing_dep_list = ["conj", "dobj", "pobj", "ROOT", "nsubj"]
    #verb_dep_list = ["xcomp"]
    print("STEP: " + step.step_text)



    spacy_doc = nlp(step.step_text.lower())


    ingredients = []
    materials = []
    verbs = []

    #spacy_doc = spacy_doc[1:]


    print("NOUN PHRASES")
    for chunk in spacy_doc.noun_chunks:
        print("TEXT: " + chunk.text, "ROOT: " + chunk.root.text, "ROOT DEP: " + chunk.root.dep_, "ROOT HEAD: " + chunk.root.head.text)
        if any(x == chunk.root.dep_ for x in ing_dep_list) and not any(x in chunk.text for x in noun_stop_words) and chunk.text not in ingredients:
            if chunk.root.text.lower() in food_list and not checkList(chunk.root.text, ingredients):
                ingredients.append(chunk.text)
        if any(x == chunk.root.dep_ for x in ing_dep_list) and chunk.text not in ingredients and not any(x in chunk.text for x in noun_stop_words) and chunk.text not in materials:
            if chunk.root.lemma_.lower() in cooking_utensils and not checkList(chunk.root.text, materials):
                materials.append(chunk.text)

    print("FIRST ITERATION: " + str(ingredients))
    print("FIRST ITERATION: " + str(materials))

    print("TOKENS")
    for token in spacy_doc:
        print("TEXT: " + token.text, "HEAD: " + token.head.text, "POS: " + token.pos_, "TAG: " + token.tag_, "DEP: " + token.dep_)
        if token.pos_ == "VERB" and token.dep_ != "xcomp" and token.text not in descriptions:
            verbs.append(token.lemma_)
        if token.pos_ == "NOUN" and token.text.lower() in food_list and token.lemma_ not in ingredients and token.text not in noun_stop_words:
            if not checkList(token.text, ingredients):
                ingredients.append(token.text)
        if token.pos_ == "NOUN" and token.text.lower() in cooking_utensils and token.lemma_ not in materials and token.text not in materials:
            if not checkList(token.text, materials):
                materials.append(token.text)

    print(ingredients)
    print(materials)
    print(verbs)
    step.ingredients = ingredients
    step.materials = materials
    step.actions = verbs

def buildStepsArray(instructions):
    steps_array = []

    for c, element in enumerate(instructions):
        #print("Loading Step " + str(c+1))
        step = recipeStep(c+1, element)
        setStepFields(step)
        steps_array.append(step)

    return steps_array

# #filtered = [token.text for token in spacy_doc if token.is_stop == False and token.text.isalpha() == True]

# print(ingredients)
# print(materials)
# print(verbs)

link = "https://www.allrecipes.com/recipe/8539106/yaki-udon/"
link = "https://www.allrecipes.com/recipe/8509102/chicken-al-pastor/"
nlp2 = stanza.Pipeline(lang='en', verbose=False)

recipe_ingredients(link)

buildFullFoodList()

scraper = scrape_me(link, wild_mode = True)
instructions = scraper.instructions_list()


new_instructions_list = []
for instruction in instructions:
    new_instructions_list += sent_tokenize(instruction)

nlp = spacy.load("en_core_web_sm")


steps_array = buildStepsArray(new_instructions_list)


for i in steps_array:
    print(i)

print(food_list)

#step_example = "Whisk together oyster sauce, soy sauce, mirin, rice vinegar, Worcestershire, sesame oil, sugar, Sriracha, and garlic in a small bowl; set aside."
#step_example = "Remove root ends from scallions and discard."
#step_example = "Chop whites and light greens into 2-inch pieces and quarter pieces lengthwise; set aside."
#step_example = "Thinly slice remaining dark greens of scallions and reserve for garnish."
#step_example = "Heat extra virgin olive oil in a skillet over medium heat."
#step_example = "Cook and stir onion, red pepper, celery, and a pinch of salt in hot oil until onion is soft and translucent, about 5 minutes."
#step_example = "Add capers; cook and stir until fragrant, about 2 minutes. Remove from heat and cool to room temperature."
#step_example = "Stir salmon, onion mixture, mayonnaise, 1/4 cup bread crumbs, garlic, mustard, cayenne, seafood seasoning, salt, and ground black pepper together in a bowl until well-mixed."
#step_example = "Cover the bowl with plastic wrap and refrigerate until firmed and chilled, 1 to 2 hours."


##https://www.allrecipes.com/recipe/8539106/yaki-udon/
##Step 1: Whisk together oyster sauce, soy sauce, mirin, rice vinegar, Worcestershire, sesame oil, sugar, Sriracha, and garlic in a small bowl; set aside.

##Step 2: Remove root ends from scallions and discard.

##Step 3: Chop whites and light greens into 2-inch pieces and quarter pieces lengthwise; set aside.

##Step 4: Thinly slice remaining dark greens of scallions and reserve for garnish.