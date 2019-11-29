import nltk
from nltk.corpus import treebank
#import networkx as nx
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

import wikipedia
#pip install nltk
#pip install networkx
#pip install nose
#pip install numpy

# GENSIM?! Topic Modelling https://radimrehurek.com/gensim/
# TextRank: https://github.com/davidadamojr/TextRank

def search_in_wiki(keyword):
    wikipedia.set_lang("en")
    tts_text = str(wikipedia.summary(keyword, sentences=3))
    return tts_text

tts_text = search_in_wiki("global warming")

tokens = nltk.word_tokenize(tts_text)
tagged = nltk.pos_tag(tokens)
nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
entities = nltk.chunk.ne_chunk(tagged)

freq = nltk.FreqDist(tokens)
for key,val in freq.items(): 
    print (str(key) + ':' + str(val))

clean_tokens = tokens[:] 
sr = stopwords.words('english')
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)
    
print("\n\n Tokens: " + str(tokens))
print("\n\n Tagged: " + str(tagged))
print("\n\n Entities: " + str(entities))
print("\n\n Freqs: " + str(freq))
print("\n\n Clean Tokens: " + str(clean_tokens))
print("\n\n Nouns: " + str(nouns))

lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in clean_tokens]
print("\n\n Lemma: " + str(lemmatized_words))