#import nltk
#from nltk import pos_tag, sent_tokenize, word_tokenize, RegexpParser
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import stanza
#stanza.download('en')
nlp = stanza.Pipeline(lang='en', verbose=False)

sample_text = "Whisk together oyster sauce, soy sauce, mirin, rice vinegar, Worcestershire, sesame oil, sugar, Sriracha, and garlic in a small bowl; set aside."

doc = nlp(sample_text)
tree = doc.sentences[0].constituency
#tree.pformat()
#tagged = pos_tag(word_tokenize(sample_text))

#entities = nltk.ne_chunk(tagged)

#print(entities)

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

printTree(tree)