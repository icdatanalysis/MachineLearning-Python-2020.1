#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 02:17:10 2019

@author: r4ph
"""

# Importando os pacotes
import re
import pandas as pd
import seaborn as sns
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.externals import joblib


# Funções Auxiliares:
# Removendo as tags htmls:
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Removendo alguns caracteres especiais como colchetes
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

# Função que remove os caracteres especiais:
def remove_special_characters(text, remove_digits=True):
    pattern=r'[^a-zA-z0-9\s]'
    text=re.sub(pattern,'',text)
    return text


# Função que limpa o texto
def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = remove_special_characters(text)
    return text

# Importanto os dados
# Fonte: https://github.com/minerandodados/mdrepo
df = pd.read_csv('data/imdb_dataset.csv', encoding ='utf-8')

df.head(5)

df.info()

df.describe()

# Selecionando somente uma amostra dos dados
df = df.groupby('sentiment').apply(lambda x: x.sample(2500))

# Visualizando a Quantidade de cada classe:
sns.countplot(x= 'sentiment',data = df)

# Aplicando função de tratamento do texto nas revisões:
df['review']=df['review'].apply(denoise_text)

# Transformando os labels em númericos:
lb = LabelBinarizer()
df['sentiment'] = lb.fit_transform(df['sentiment'])

# Definindo as variáveis dependentes/independentes:
X = df['review'].values
y = df['sentiment'].values

# Criação de um vetor que irá  calcular a frequencia de todas as palavras 
vectorizer = CountVectorizer(ngram_range=(1,2))

# Converter o texto em uma matriz de contagens de tokens
X = vectorizer.fit_transform(X)

# Dividindo os dados:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Create the model
model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(metrics.classification_report(y_test,y_pred,target_names=['Positive','Negative']))

# Salva o modelo:
joblib.dump(model, 'classifier_movies.joblib')

# Salva o Vetorizador:
joblib.dump(vectorizer, 'count_vectorizer.joblib')

# Classificando um exemplo:
example = ['Titanic is one bad movie']
_X = vectorizer.transform(example)

# Visualizando os resusltados do exemplo:
label = {0:'negative', 1:'positive'}

print('Prediction: %s\nProbability: %.2f%%' %\
      (label[model.predict(_X)[0]], 
       np.max(model.predict_proba(_X))*100))