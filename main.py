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
    global all_ingredients
    all_ingredients = []
    for i in scraper.ingredients():
        i = ingredient(i)
        buildIngredient(i)
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
    print("7. Any questions about time or temperature in the recipe\n")
    print("8. Does this recipe (as a whole) call for ingredient___?\n")
    print("9. What is a(n) ____? (Will return a Google Search to define what you're looking for)\n")
    print("10. How do I ____? (Will return a YouTube Search for a helpful video to show you how)\n")
    print("11. Read this step again\n")
    #print("- Ask questions about the current step\n")
    #print("- Ask about the ingredients or utensils\n")
    #print("- Ask about the actions you need to perform\n")
    print("If you even need a refresher on these simply type 'help' in the chat")

def printSteps(recipe_steps):
    for element in recipe_steps:
        print(element)

def printIngredients(ingredients):
    for i in ingredients:
        print(i)

def printAllIngredients(ingredients):
    for i in ingredients:
        print(i.ingredient_text)

def related(chat_in):
    chat_in = chat_in.lower()
    chat_out = []

    exit_conditions = ["quit"]
    help_conditions = ["help"]

    #print(chat_in)

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
        #print(chat_in)
        chat_out = []
        chat_out.append("2")
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
        doc = nlp(chat_in.lower())
        i_string = []
        
        for word in doc.sentences[0].words[2:]:
            if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
                i_string.append(word.text)
        #print(i_string)
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
    elif "all" in chat_in and "ingredients" in chat_in:
        chat_out = []
        chat_out.append("6")
    elif "temperature" in chat_in or "time" in chat_in or "minutes" in chat_in or "farenheit" in chat_in or "heat" in chat_in or "how long" in chat_in:
        chat_out = []
        chat_out.append("7")
    elif "how do i" in chat_in:
        chat_out = []
        chat_out.append("10")
        my_regex = ".+(how do i)"
        new_str = re.sub(my_regex, "", chat_in)
        print(new_str)
        chat_out.append(new_str)
    elif "what is" in chat_in or "what's a" in chat_in or "whats a" in chat_in or "what's an" in chat_in or "whats an" in chat_in:
        chat_out = []
        chat_out.append("9")
        chat_out.append(chat_in)
    elif "need" in chat_in or "do I" in chat_in or "call for" in chat_in:
        chat_out = []
        chat_out.append("8")

        bool = False

        doc = nlp(chat_in.lower())
        i_string = []
        
        for word in doc.sentences[0].words[2:]:
            if word.xpos == "NN" or word.xpos == "NNS" or word.xpos == "NNP":
                i_string.append(word.text)

        temp = [] 

        for i in all_ingredients:
            print(i.food_item)
            for x in i_string:
                if x in i.food_item:
                    if i.ingredient_text != temp:
                        if i.ingredient_text is not "recipe":
                            temp.append(i.ingredient_text)
                            bool = True
        chat_out.append(bool)

        if not bool:
            i_str = " ".join(i_string)
            chat_out.append(i_str)
        else:
            for i in temp:
                chat_out.append(i)
        

    
    elif "current" in chat_in:
        chat_out = []
        chat_out.append("11")
    else:
        chat_out = []
        chat_out.append("1234567890")
    return chat_out

def runChatbot():
    print("Welcome to Recipe Extravaganza!\n")
    printHelp()
    #recipe = input("Please give me a link to a recipe:\n")
    #print("\nHoly Guacamole! That sounds yummy. To start you off here are the list of ingredients you will need:\n")
    #print(recipe_scraper(recipe))
    booli = True
    while booli:
        try:
            recipe = input("Please give me a link to a recipe:\n")
            instructions_list = recipe_scraper(recipe)
            booli = False
        except:
            print("\nWhat, are you baked? You didn't give us a good link! Please try again\n")
            
    print("\nHoly Guacamole! That sounds yummy. To start you off here are the list of ingredients you will need:\n")

    recipe_ingredients(recipe)
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
            break
        #chatbot help
        if query[0] == "help":
            printHelp()
        if query[0] == "next":
            if recipe_pointer >= len(recipe_steps) - 1:
                print("\nWe've reached the end of our recipe, Bon Appetit!")
            else:
                recipe_pointer += 1
                print("\n", recipe_steps[recipe_pointer])
        elif query[0] == "2":
            if recipe_pointer == 0:
                print("\nSorry we can't go back a step, we are at Step #0")
            else:
                recipe_pointer -= 1
                print("\n", recipe_steps[recipe_pointer])
        elif query[0] == "3":
            print("\nSure! Here are the ingredients you need for this step:\n")
            printIngredients(recipe_steps[recipe_pointer].ingredients)
        elif query[0] == "4":
            print("\nNo problemo. Here are the materials you will need here:\n")
            print(recipe_steps[recipe_pointer].materials)
        elif query[0] == "5" and len(query) >= 2:
            l = len(query)
            for i in range(1, l):
                print("\nYou need", query[i])
            # for i in all_ingredients:
            #     temp = i.ingredient.split(" ")
            #     for word in temp:
            #         if x == word:
            #             print("\nYou need", i.ingredient)
            #             break
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
    
def YoutubeSearch(stringg):
    temp = stringg.split(" ")
    text = "how+to+"
    text = text + "+".join(temp)
    url = 'https://www.youtube.com/results?search_query=' + text
    
    request_result=requests.get( url )
    # Creating soup from the fetched request
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    #return(soup)
    # heading_object=soup.find_all( 'h3' )

    # # Iterate through the object 
    # # and print it as a string.
    # for info in heading_object:
    #print(info.getText())
    #print("------")
    #soup = BeautifulSoup(r.content, 'html5lib')
    text = soup.get_text()
    return(url)


if __name__ == "__main__":
    # print("Start of Program")
    # # yaki udon
    #instructions_list = recipe_scraper("https://www.allrecipes.com/recipe/8539106/yaki-udon/")
    # #print(instructions_list)

    # #text = "fold butter into flour"
    # text = "whisk vigorously"
    # print(GoogleSearchDefinition(text))
    #recipe = "https://www.allrecipes.com/recipe/8539106/yaki-udon/"
    #recipe_ingredients(recipe)
    #for i in all_ingredients:
        #print(i)

    #new_instructions_list = []
    #for instruction in instructions_list:
    #    new_instructions_list += sent_tokenize(instruction)

    # #print(new_instructions_list)
    # # recipe_steps hold our array of Step classes for navigation
    #recipe_steps = buildStepsArray(new_instructions_list)
    #printSteps(recipe_steps)
    # #printSteps(recipe_steps)

    runChatbot()
   