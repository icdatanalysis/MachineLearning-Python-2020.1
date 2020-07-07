# To add a new cell, type ''
# To add a new markdown cell, type ''

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Lemmatization
# In contrast to stemming, lemmatization looks beyond word reduction, and considers a language's full vocabulary to apply a *morphological analysis* to words. The lemma of 'was' is 'be' and the lemma of 'mice' is 'mouse'. Further, the lemma of 'meeting' might be 'meet' or 'meeting' depending on its use in a sentence.


# Perform standard imports:
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()



doc1 = nlp(u"I am a runner running in a race because I love to run since I ran today")

for token in doc1:
    print(token.text, '\t', token.pos_, '\t', token.lemma, '\t', token.lemma_)


# <font color=green>In the above sentence, `running`, `run` and `ran` all point to the same lemma `run` (...11841) 
# to avoid duplication.</font>

# ### Function to display lemmas
# Since the display above is staggared and hard to read, let's write a function that displays the information we want more neatly.


def show_lemmas(text):
    for token in text:
        print(f'{token.text:{12}} {token.pos_:{6}} {token.lemma:<{22}} {token.lemma_}')


# Here we're using an **f-string** to format the printed text by setting minimum field widths and adding a left-align to the lemma hash value.


doc2 = nlp(u"I saw eighteen mice today!")

show_lemmas(doc2)


# <font color=green>Notice that the lemma of `saw` is `see`, `mice` is the plural form of `mouse`, and yet `eighteen` is its own number, *not* an expanded form of `eight`.</font>


doc3 = nlp(u"I am meeting him tomorrow at the meeting.")

show_lemmas(doc3)


# <font color=green>Here the lemma of `meeting` is determined by its Part of Speech tag.</font>


doc4 = nlp(u"That's an enormous automobile")

show_lemmas(doc4)


# <font color=green>Note that lemmatization does *not* reduce words to their most basic synonym - that is, 
# `enormous` doesn't become `big` and `automobile` doesn't become `car`.</font>

# We should point out that although lemmatization looks at surrounding text to determine a given word's part of speech, 
# it does not categorize phrases. In an upcoming lecture we'll investigate *word vectors and similarity*.
# 
# ## Next up: Stop Words

