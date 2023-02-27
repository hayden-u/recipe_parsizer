# main file
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
#stanza.download('en')
nlp = stanza.Pipeline(lang='en', verbose=False)

# to get ingredients for each step, 
def printPOS(doc):
    #POS tags
    print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')
    return 

def printRelation(doc):
    #depparse
    print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')


# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n" + "Step Ingredients: " + str(self.ingredients)
        
#ingredients will be a field of recipe step, with step 0 holding all of the ingredients
class ingredient:
    def __init__(self, ingredient):
        self.ingredient = ingredient
        temp = ingredient.split()
        self.quantity = temp[0]
        if temp[0].isnumeric():
            self.quantity = int(self.quantity)
        self.unit = temp[1]

    def __str__(self):
        return "Ingredient: " + str(self.ingredient) + " | Quantity: " + str(self.quantity) 

def recipe_scraper(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    return scraper.instructions_list()

# def findStepIngredients(stepClass):
#     #function will find each individual ingredient in the given step
#     # then populate the step class ingredient field
#     text = stepClass.step_text.lower()
#     document = nlp(text)
#     ingredient_list = []
#     for sent in document.sentences:
#         for word in sent.words:
#             if word.upos == "NOUN":
#                 ing_dict = { "text": word.text,
#                              "id" : word.id,
#                              "head": word.head}
#                 ingredient_list.append(ing_dict)
#     #printPOS(document)
#     #printRelation(document)
#     #pos_tagged = nltk.pos_tag(tokenized)
#     #print(pos_tagged)
#     #print(ingredient_list)
#     pass


def traverseTree(root, some_list):
    #print(some_list)
    if root.label == "NP":
        full_str = ""
        for child in root.children:
            if child.label == "NN" or child.label == "NNS":
                for c in child.children:
                    full_str = full_str + str(c.label) + " "                
            else:
                continue
        if full_str != "":
            some_list.append(full_str[0:len(full_str)-1])

    for child in root.children:
        traverseTree(child, some_list)

    return some_list

def findStepIngredients(stepClass):
    doc = nlp(stepClass.step_text.lower())
    tree = doc.sentences[0].constituency
    some_list = []
    stepClass.ingredients = traverseTree(tree, some_list)

def buildStepsArray(instructions):
    steps_array = []

    for c, element in enumerate(instructions):
        #print("Loading Step " + str(c+1))
        step = recipeStep(c+1, element)
        findStepIngredients(step)
        steps_array.append(step)

    return steps_array

def recipe_ingredients(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    global all_ingredients
    all_ingredients = []
    for i in scraper.ingredients():
        i = ingredient(i)
        all_ingredients.append(i)
    return

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
    print("9. How do I perform ___ cooking task?\n")
    #print("- Ask questions about the current step\n")
    #print("- Ask about the ingredients or utensils\n")
    #print("- Ask about the actions you need to perform\n")
    print("If you even need a refresher on these simply type 'help' in the chat")

def printSteps(recipe_steps):
    for element in recipe_steps:
        print(element)

def printIngredients(ingredients):
    for i in ingredients:
        print(i.ingredient)

def runChatbot():
    print("Welcome to Recipe Extravaganza!\n")
    printHelp()
    recipe = input("Please give me a link to a recipe:\n")
    print("Holy Guacamole! That sounds yummy. To start you off here are the list of ingredients you will need:\n")
    #print(recipe_scraper(recipe))
    instructions_list = recipe_scraper(recipe)
    recipe_ingredients(recipe)
    printIngredients(all_ingredients)
    term_size = os.get_terminal_size()
    print('=' * term_size.columns)
    print("\nWhat else can I do for you?\n")

    recipe_steps = buildStepsArray(instructions_list)

    exit_conditions = ["quit"]
    help_conditions = ["help"]
    recipe_pointer = 0
    
    
    while True:
        x = "sesame"
        query = input("")
        #chatbot exit
        if query in exit_conditions:
            break
        #chatbot help
        if query in help_conditions:
            printHelp()
        if query == "next":
            if recipe_pointer >= len(recipe_steps) - 1:
                print("\nWe've reached the end of our recipe, Bon Appetit!")
            else:
                recipe_pointer += 1
                print("\n", recipe_steps[recipe_pointer])
        elif query == "2":
            if recipe_pointer == 0:
                print("\nSorry we can't go back a step, we are at Step #0")
            else:
                recipe_pointer -= 1
                print("\n", recipe_steps[recipe_pointer])
        elif query == "3":
            print("\nSure! Here are the ingredients you need for this step:\n")
            printIngredients(recipe_steps[recipe_pointer].ingredients)
        elif query == "4":
            print("\nNo problemo. Here are the materials you will need here:\n")
            print(recipe_steps[recipe_pointer].materials)
        elif query == "5": ##pretend x is input of ingredient they are asking for
            for i in all_ingredients:
                temp = i.ingredient.split(" ")
                for word in temp:
                    if x == word:
                        print("\nYou need", i.ingredient)
                        break
        elif query == "6":
            print("\nHere’s the full list of ingredients for this recipe:\n")
            printIngredients(all_ingredients)
        elif query == "7":
            print("\n", recipe_steps[recipe_pointer])
        elif query == "8": ##pretend x is input of ingredient they are asking for
            bool = False
            for i in all_ingredients:
                temp = i.ingredient.split(" ")
                for word in temp:
                    if x == word:
                        bool = True
            if bool:
                print("\nYes, this recipe does include", x)
            else:
                print("\nNo, this recipe does not include", x)
        elif query == "9":
            text = "fold butter into flour"
            print("\nHere's a link to what Google foud as the definition of the action you want clarity on:\n")
            print(GoogleSearchDefinition(text))
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
    #text = "+definition".join(temp)
    # print(temp)
    # length = len(temp)
    # text = ""
    # for word in temp:
    #     text = text.join(temp[i])
    #     text = text.join("+")
    # text = text.join(temp[length-1])   

    #print(text) 
    
    url = 'https://google.com/search?q=' + text
  
    # Fetch the URL data using requests.get(url),
    # store it in a variable, request_result.
    request_result=requests.get( url )
  
    # Creating soup from the fetched request
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    #return(soup)    
    # heading_object=soup.find_all( 'h3' )
  
    # # Iterate through the object 
    # # and print it as a string.
    # for info in heading_object:
    #     print(info.getText())
    #     print("------")
    #soup = BeautifulSoup(r.content, 'html5lib')
    text = soup.get_text()
    return(url)
    



if __name__ == "__main__":
    # print("Start of Program")
    # # yaki udon
    instructions_list = recipe_scraper("https://www.allrecipes.com/recipe/8539106/yaki-udon/")
    # #print(instructions_list)

    # #text = "fold butter into flour"
    # text = "whisk vigorously"
    # print(GoogleSearchDefinition(text))
    recipe = "https://www.allrecipes.com/recipe/8539106/yaki-udon/"
    recipe_ingredients(recipe)
    for i in all_ingredients:
        print(i)

    new_instructions_list = []
    for instruction in instructions_list:
        new_instructions_list += sent_tokenize(instruction)

    # #print(new_instructions_list)
    # # recipe_steps hold our array of Step classes for navigation
    recipe_steps = buildStepsArray(new_instructions_list)
    printSteps(recipe_steps)
    # #printSteps(recipe_steps)

    #runChatbot()
   