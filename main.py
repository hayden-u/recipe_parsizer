# main file HAYDEN hhh
from recipe_scrapers import scrape_me
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
import stanza
import requests
import bs4
import re
import os
stanza.download('en')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

nlp_spacy = spacy.load("en_core_web_sm")
nlp_stanza = stanza.Pipeline(lang='en', verbose=False)

#list of words used for processing
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
        'plastic wrap', 'wrap', 'dish', 'board', 'cutting board', 'grill', 'smoker']

# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
        self.actions = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n"
        
#ingredients will be a field of recipe step, with step 0 holding all of the ingredients
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

#scrape webpage
def recipe_scraper(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    return scraper.instructions_list()

#helper to check if word is already present in a list
def checkList(text, list):
    is_present = False
    for element in list:
        if text in element:
            is_present = True
    return is_present

#sets up the Step Class fields
def setStepFields(step):

    noun_stop_words = ["heat", "temperature", "cool", "garnish", "lengthwise", "degrees"]
    ing_dep_list = ["conj", "dobj", "pobj", "ROOT", "nsubj"]
    #verb_dep_list = ["xcomp"]
    spacy_doc = nlp_spacy(step.step_text.lower())
    
    ingredients = []
    materials = []
    verbs = []

    for chunk in spacy_doc.noun_chunks:
        #print("TEXT: " + chunk.text, "ROOT: " + chunk.root.text, "ROOT DEP: " + chunk.root.dep_, "ROOT HEAD: " + chunk.root.head.text)
        if any(x == chunk.root.dep_ for x in ing_dep_list) and not any(x in chunk.text for x in noun_stop_words) and chunk.text not in ingredients:
            if chunk.root.text.lower() in food_list and not checkList(chunk.root.text, ingredients):
                ingredients.append(chunk.text)
        if any(x == chunk.root.dep_ for x in ing_dep_list) and chunk.text not in ingredients and not any(x in chunk.text for x in noun_stop_words) and chunk.text not in materials:
            if chunk.root.lemma_.lower() in cooking_utensils and not checkList(chunk.root.text, materials):
                materials.append(chunk.text)

    for token in spacy_doc:
        #print("TEXT: " + token.text, "HEAD: " + token.head.text, "POS: " + token.pos_, "TAG: " + token.tag_, "DEP: " + token.dep_)
        if token.pos_ == "VERB" and token.dep_ != "xcomp" and token.text not in descriptions:
            verbs.append(token.lemma_)
        if token.pos_ == "NOUN" and token.text.lower() in food_list and token.lemma_ not in ingredients and token.text not in noun_stop_words:
            if not checkList(token.text, ingredients):
                ingredients.append(token.text)
        if token.pos_ == "NOUN" and token.text.lower() in cooking_utensils and token.lemma_ not in materials and token.text not in materials:
            if not checkList(token.text, materials):
                materials.append(token.text)

    step.ingredients = ingredients
    step.materials = materials
    step.actions = verbs
    return

#builds a step class array
def buildStepsArray(instructions):
    steps_array = []

    for c, element in enumerate(instructions):
        #print("Loading Step " + str(c+1))
        step = recipeStep(c+1, element)
        setStepFields(step)
        steps_array.append(step)

    return steps_array

#sets ingredient class fields
def buildIngredient(ingredient):
    #print("Ingredient Text: " + ingredient.ingredient_text)
    my_regex = my_regex = "\s\(.*?\)"
    new_str = re.sub(my_regex, "", ingredient.ingredient_text)
    #print("Regexed String: " + new_str + "\n")
    doc = nlp_stanza(new_str.lower())
    i_string = ""
    
    for word in doc.sentences[0].words[2:]:
        if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
            i_string = i_string + " " + word.text
    ingredient.food_item = i_string
    return

#build string of all ingredients
def buildFullFoodList():
    global food_list
    food_list = []
    for ing in all_ingredients:
        for word in ing.food_item.split():
            if word not in unnecessaryDescriptions:
                food_list.append(word)

    food_list = " ".join(food_list)
    return

#build ingredients Class for all ingredients
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

#help prints
def printHelp():
    print("Here is a list of possible ways you can interact with me\n")
    print("1. Next Step\n")
    print("2. Previous Step\n")
    print("3. What ingredient(s) do I need here\n")
    print("4. What material(s) do I need here?\n")
    print("5. How much of ingredient ___ do I need?\n")
    print("6. What are all of the ingredients needed for this recipe?\n")
    print("7. Any questions about time or temperature in the recipe\n")
    print("8. Does this recipe (as a whole) call for ingredient___?\n")
    print("9. What is a(n) ____? (Will return a Google Search to define what you're looking for)\n")
    print("10. How do I ____? (Will return a YouTube Search for a helpful video to show you how)\n")
    print("11. Read this step again\n")
    print("If you even need a refresher on these simply type 'help' in the chat")
    print('To quit simple type "quit"\n')

def printSteps(recipe_steps):
    for element in recipe_steps:
        print(element)

def printList(list):
    for i in list:
        print(i)

def printAllIngredients(ingredients):
    for i in ingredients:
        print(i.ingredient_text)

#chatbot input handling
def related(chat_in):
    chat_in = chat_in.lower()
    chat_out = []

    exit_conditions = ["quit"]
    help_conditions = ["help"]

    for i in exit_conditions:
        if i in chat_in:
            chat_out = []
            chat_out.append("exit")
            return chat_out
    for i in help_conditions:
        if i in chat_in:
            chat_out = []
            chat_out.append("help")
            return chat_out
    
    if "next" in chat_in:
        chat_out = []
        chat_out.append("next")
    elif "previous" in chat_in or "back" in chat_in:
        chat_out = []
        chat_out.append("2")
    elif "all" in chat_in and "ingredients" in chat_in:
        chat_out = []
        chat_out.append("6")
    elif "what" in chat_in and ("ingredient" in chat_in or "ingredients" in chat_in) :
        chat_out = []
        chat_out.append("3")
    elif "what" in chat_in and ("material" in chat_in or "materials" in chat_in or "utencils" in chat_in or "untencil" in chat_in) :
        chat_out = []
        chat_out.append("4")
    elif "how much" in chat_in or "amount" in chat_in or "how many" in chat_in:
        chat_out = []
        chat_out.append("5")
        bool = False
        doc = nlp_stanza(chat_in.lower())
        i_string = []
        
        for word in doc.sentences[0].words[2:]:
            if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
                i_string.append(word.text)

        for i in all_ingredients:
            for noun in i_string:
                if noun in i.food_item:
            # temp = i.food_item.split(" ")
            # for word in temp:
            #     if word in chat_in:
                    # print("\nNoun:", noun)
                    # print("i:", i.food_item)
                    if i.ingredient_text not in chat_out:
                        chat_out.append(i.ingredient_text)
                    bool = True
        if not bool:
            chat_out.append("it all")
    elif "temperature" in chat_in or "time" in chat_in or "minutes" in chat_in or "farenheit" in chat_in or "heat" in chat_in or "how long" in chat_in:
        chat_out = []
        chat_out.append("7")
    elif "how do i" in chat_in or "how do you" in chat_in or "how does one" in chat_in:
        chat_out = []
        chat_out.append("10")
        my_regex = ".+(how do i)"
        new_str = re.sub(my_regex, "", chat_in)
        chat_out.append(new_str)
    elif "what is" in chat_in or "what's a" in chat_in or "whats a" in chat_in or "what's an" in chat_in or "whats an" in chat_in:
        chat_out = []
        chat_out.append("9")
        chat_out.append(chat_in)
    elif "need" in chat_in or "do I" in chat_in or "call for" in chat_in or "recipe include" in chat_in:
        chat_out = []
        chat_out.append("8")

        bool = False

        doc = nlp_stanza(chat_in.lower())
        i_string = []
        
        for word in doc.sentences[0].words[2:]:
            if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
                i_string.append(word.text)

        temp = [] 

        for i in all_ingredients:
            #print(i.food_item)
            for x in i_string:
                if x in i.food_item:
                    if i.ingredient_text != temp:
                        temp.append(i.ingredient_text)
                        bool = True
        chat_out.append(bool)

        if not bool:
            i_str = " ".join(i_string)
            chat_out.append(i_str)
        else:
            for i in temp:
                chat_out.append(i)
        

    
    elif "current" in chat_in or "repeat" in chat_in:
        chat_out = []
        chat_out.append("11")
    else:
        chat_out = []
        chat_out.append("1234567890")
    return chat_out

#chatbot run
def runChatbot():
    print("Welcome to Recipe Extravaganza! My name is Reece\n")
    printHelp()

    booli = True
    while booli:
        try:
            recipe = input("Please give me a link to a recipe:\n")
            if recipe == "quit":
                print("Gone so soon? Come back with a recipe, have a nice day.")
                return
            instructions_list = recipe_scraper(recipe)
            booli = False
        except:
            #print("\nWhat, are you baked? You didn't give us a good link! Please try again\n")
            print("\nHmm not sure I can read that link. We recommend you give us a recipe from one of these websites:\nFoodNetwork.com\nAllRecipes.com\nTasteOfHome.com\nDelish.com\n")
            
    recipe_ingredients(recipe)
    buildFullFoodList()

    print("\nHoly Guacamole!", recipe_title, "sounds yummy. To start you off here are the list of ingredients you will need:\n")

    printAllIngredients(all_ingredients)


    new_instructions_list = []
    for instruction in instructions_list:
        new_instructions_list += sent_tokenize(instruction)

    recipe_steps = buildStepsArray(new_instructions_list)

    print("\nHere's the first step on your journey to a full belly:\n")
    recipe_pointer = 0
    print("\n", recipe_steps[recipe_pointer])

    term_size = os.get_terminal_size()
    print('=' * term_size.columns)
    print("\nWhat else can I do for you?\n")   
    
    while True:
        query = input("")
        query = related(query)
        #x = "sesame"
        #chatbot exit
        #print(query)
        if query[0] == "exit":
            print("Thanks for talking with me, have a nice meal!")
            break
        #chatbot help
        if query[0] == "help":
            printHelp()
        elif query[0] == "next":
            if recipe_pointer >= len(recipe_steps) - 1:
                print("\nWe've reached the end of our recipe, Bon Appetit!")
            else:
                recipe_pointer += 1
                print("\n", recipe_steps[recipe_pointer])
        elif query[0] == "2":
            if recipe_pointer == 0:
                print("\nSorry we can't go back a step, we are at Step #1")
            else:
                recipe_pointer -= 1
                print("\n", recipe_steps[recipe_pointer])
        elif query[0] == "3":
            if len(recipe_steps[recipe_pointer].ingredients) == 0:
                print("\nI can't find any specific ingredients for this step. Here is a list of them all:\n")
                printAllIngredients(all_ingredients)
            else:
                print("\nSure! Here are the ingredients you need for this step:\n")
                printList(recipe_steps[recipe_pointer].ingredients)
        elif query[0] == "4":
            if len(recipe_steps[recipe_pointer].materials) == 0:
                print("\nI can't find any specific materials for this step.")
            else:
                print("\nNo problemo. Here are the materials you will need here:\n")
                printList(recipe_steps[recipe_pointer].materials)
        elif query[0] == "5" and len(query) >= 2:
            l = len(query)
            for i in range(1, l):
                print("\nYou need", query[i])
        elif query[0] == "6":
            print("\nHere’s the full list of ingredients for this recipe:\n")
            printAllIngredients(all_ingredients)
        elif query[0] == "7":
            print("\n", recipe_steps[recipe_pointer])
        elif query[0] == "8": ##pretend x is input of ingredient they are asking for
            bool = query[1]
            l = len(query)
            x = query[2]
            if not bool:
                print("\nNo, this recipe does not include", x)
            else:
                print("\nYes, this recipe does include", x)
                if l != 3:
                    for i in range(3, l):
                        print("&", query[i])
                    
                
        elif query[0] == "9" and len(query) >= 2:
            text = query[1]
            print("\nHere's a link to what Google foud as the definition of the action you want clarity on:\n")
            print(GoogleSearchDefinition(text))
        elif query[0] == "10" and len(query) >= 2:
            text = query[1]
            print("\nHere's a link to a helpful Youtube Search for a video that can show you how to", text, ":\n")
            print(YoutubeSearch(text))
        elif query[0] == "11":
            print("\n", recipe_steps[recipe_pointer])
        else:
            print("\nI’m sorry, I do not understand your question. Here is the help menu for a list of questions I know how to answer:\n")
            printHelp()
        
        term_size = os.get_terminal_size()
        print('=' * term_size.columns)
        print("\nWhat else can I do for you?\n")


def GoogleSearchDefinition(stringg):
    # Make two strings with default google search URL
    # 'https://google.com/search?q=' and
    # our customized search keyword.
    # Concatenate them

    temp = stringg.split(" ")
    text = "+".join(temp)
    text = text + "+definition"
    
    url = 'https://google.com/search?q=' + text
  
    # Fetch the URL data using requests.get(url),
    # store it in a variable, request_result.
    request_result=requests.get( url )
  
    # Creating soup from the fetched request
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    text = soup.get_text()
    return(url)
    
def YoutubeSearch(stringg):
    temp = stringg.split(" ")
    #text = "how+to+"
    text = "+".join(temp)
    url = 'https://www.youtube.com/results?search_query=' + text
    
    request_result=requests.get( url )
    # Creating soup from the fetched request
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
 
    text = soup.get_text()
    return(url)


if __name__ == "__main__":
    runChatbot()
   