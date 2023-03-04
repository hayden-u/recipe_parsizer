import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.symbols import nsubj, VERB

stop = STOP_WORDS

# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n" + "Step Ingredients: " + str(self.ingredients)


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
nlp = spacy.load("en_core_web_sm")

step_example = "Whisk together oyster sauce, soy sauce, mirin, rice vinegar, Worcestershire, sesame oil, sugar, Sriracha, and garlic in a small bowl; set aside."
#step_example = "Remove root ends from scallions and discard."
#step_example = "Chop whites and light greens into 2-inch pieces and quarter pieces lengthwise; set aside."
#step_example = "Thinly slice remaining dark greens of scallions and reserve for garnish."
#step_example = "Heat extra virgin olive oil in a skillet over medium heat."
#step_example = "Cook and stir onion, red pepper, celery, and a pinch of salt in hot oil until onion is soft and translucent, about 5 minutes."
#step_example = "Add capers; cook and stir until fragrant, about 2 minutes. Remove from heat and cool to room temperature."
#step_example = "Stir salmon, onion mixture, mayonnaise, 1/4 cup bread crumbs, garlic, mustard, cayenne, seafood seasoning, salt, and ground black pepper together in a bowl until well-mixed."
#step_example = "Cover the bowl with plastic wrap and refrigerate until firmed and chilled, 1 to 2 hours."

spacy_doc = nlp(step_example)

ingredients = []
materials = []
for chunk in spacy_doc.noun_chunks:
    #print("TEXT: " + chunk.text, "ROOT: " + chunk.root.text, "DEP: " + chunk.root.dep_, "ROOT HEAD: " + chunk.root.head.text)
    if chunk.root.dep_ == "conj" or chunk.root.dep_ == "dobj":
        ingredients.append(chunk.text)
    if chunk.root.dep_ == "pobj":
        materials.append(chunk.text)
#filtered = [token.text for token in spacy_doc if token.is_stop == False and token.text.isalpha() == True]

verbs = set()
for pos_sub in spacy_doc:
    if pos_sub.dep == nsubj and pos_sub.head.pos == VERB:
        verbs.add(pos_sub.head)
print(step_example)
print(ingredients)
print(materials)
#print(filtered)
nouns = []
verbs = []

#printTags(spacy_doc)

#printDeprel(spacy_doc)

#displacy.serve(spacy_doc, style="dep", port=5001)

## Remove stop words?


##https://www.allrecipes.com/recipe/8539106/yaki-udon/
##Step 1: Whisk together oyster sauce, soy sauce, mirin, rice vinegar, Worcestershire, sesame oil, sugar, Sriracha, and garlic in a small bowl; set aside.

##Step 2: Remove root ends from scallions and discard.

##Step 3: Chop whites and light greens into 2-inch pieces and quarter pieces lengthwise; set aside.

##Step 4: Thinly slice remaining dark greens of scallions and reserve for garnish.