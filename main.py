# main file
from recipe_scrapers import scrape_me

def recipe_scraper(recipe_link):
    scraper = scrape_me(recipe_link, wild_mode = True)
    rec1 = Recipe(scraper.ingredients())
    return rec1

class Step():

    def __init__(self, ingredients, utensils):
        self.ingredients = ingredients
        self.utensils = utensils

class Recipe():

    def __init__(self, ingredients):
        self.ingredients = ingredients


if __name__ == "__main__":
    print("Welcome to Recipe Extravaganza!\n")
    print("Here is a list of possible ways you can interact with me\n")
    print("- Go to next or previous step\n")
    print("- Ask questions about the current step\n")
    print("- Ask about the ingredients or utensils\n")
    print("If you even need a refresher on these simply type 'help' in the chat")
    recipe = input("Please give me a link to a recipe:\n")
    print("Holy Guacamole! That sounds yummy. To start you off here are the list of ingredients you will need:\n")
    rec1 = recipe_scraper(recipe)
    for i in rec1.ingredients:
        print(i, '\n')

    while True:
        input = input()


