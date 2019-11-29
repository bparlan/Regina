# install kernel for hydrogen run
# python -m pip install ipykernel
# python -m ipykernel install --user

# python -m pip install --upgrade pip
# python -m pip install XXX 
# pip install nltk
# pip install networkx
# pip install nose
# pip install numpy

# GENSIM?! Topic Modelling https://radimrehurek.com/gensim/
# TextRank: https://github.com/davidadamojr/TextRank

#powershell: "apm install hydrogen" komutu ile hydrogen yükle
#powershell: "easy_install https://pypi.python.org/packages/source/s/setuptools/setuptools-19.2.tar.gz" gensim için

# LDA

# T2

import string
import nltk
from nltk.corpus import stopwords
# create English stop words list
en_stop = set(stopwords.words('english'))

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

from nltk.stem.porter import PorterStemmer

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents

import wikipedia

def wikigetir(keyword):
    textpage = wikipedia.page(keyword)
    text = textpage.content
    return text

doc_a = str(wikigetir("shamanism"))
print("doc geldi")

doc_b = str(wikigetir("religion"))
print("doc geldi")

doc_set = [doc_a, doc_b]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

    print("docset loop list")

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
print("dictionary olusturuldu")   

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]
print("corpus matrix cevirildi")

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)
print("LDA Model oluşturuldu")

print("dictionary:\n" + str(stopped_tokens))
print("ldamodel:\n" + str(ldamodel))