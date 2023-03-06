import nltk
from nltk import pos_tag, sent_tokenize, word_tokenize, RegexpParser
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import stanza
#stanza.download('en'
nlp = stanza.Pipeline(lang='en', verbose=False)

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

def printTree(tree, markerStr="+- ", levelMarkers=[]):
    emptyStr = " "*len(markerStr)
    connectionStr = "|" + emptyStr[:-1]

    level = len(levelMarkers)
    mapper = lambda draw: connectionStr if draw else emptyStr
    markers = "".join(map(mapper, levelMarkers[:-1]))
    markers += markerStr if level > 0 else ""
    print(f"{markers}{tree.label}")
    for i, child in enumerate(tree.children):
        isLast = i == len(tree.children) - 1
        printTree(child, markerStr, [*levelMarkers, not isLast])

sample_text = "Remove root ends from scallions and discard."

doc = nlp(sample_text.lower())
tree = doc.sentences[0].constituency

printTree(tree)
empty_list = []
new_list = traverseTree(tree, empty_list)
print(new_list)