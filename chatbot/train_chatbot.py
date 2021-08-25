#!/usr/bin/env python3
# coding: utf8
"""
Nom: train_chatbot.py
Rôle: Crée et entraîne le modèle chatbot_model.h5 à partir des phrases et thèmes contenus dans intents.json
Auteur: Robin Clerc robin.clerc@gmail.com
Version: 1.0
Date: 25/08/2021
Licence: GPLv3.0
Usage: python3 train_chatbot.py
Autres: Dans le cadre du cours P8 IED L1 IF UOR par P. Kislin
https://data-flair.training/blogs/python-chatbot-project/
https://www.datacorner.fr/nltk/
https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
"""

# Importer les paquets
import nltk
#from nltk.stem import WordNetLemmatizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
#lemmatizer = WordNetLemmatizer()
lemmatizer = FrenchLefffLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

from nltk.corpus import stopwords

# Initialise les variables
words = []
classes = []
documents = []
#ignore_words = ['?', '!']
ignore_words = set(stopwords.words('french'))
data_file = open('intents.json').read()
# Paquet json pour analyser (parse) le fichier intents.json
intents = json.loads(data_file)

for intent in intents['intents']:
  # Itère sur chaque mot dans les motifs (patterns)
  for pattern in intent['patterns']:

    # Chaque mot devient un jeton (tokenize)
    #w = nltk.word_tokenize(pattern)
    w = nltk.word_tokenize(pattern, language="french")
    words.extend(w)
    # Ajoute documents à l'ensemble de texte (corpus)
    documents.append((w, intent['tag']))

    # Ajout à la liste de classes
    if intent['tag'] not in classes:
      classes.append(intent['tag'])

# Lemmatisation, bas de casse, supression doublons
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
# Trier les classes
classes = sorted(list(set(classes)))
# documents = combinaison de motifs et intentions
print (len(documents), "documents")
# classes = intentions (intents)
print (len(classes), "classes", classes)
# words = tous les mots, vocabulaire
print (len(words), "unique lemmatized words", words)

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Créer le jeu de donnée d'entrainement (training data)
training = []
# Créer un tableau (array) vide pour la sortie
output_empty = [0] * len(classes)
# Jeu de donnée d'entrainement (training set), groupe (bag) de mots pour chaque phrase
for doc in documents:
  # Initialise le groupe de mots
  bag = []
  # Liste de mots jetonnisés (tokenized) pour le motif
  pattern_words = doc[0]
  # Lemmatise chaque mot - crée le radical, tente de représenter les mots similaires
  pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
  # Crée le groupe de mots avec 1, si le mot correspond au motif
  for w in words:
    bag.append(1) if w in pattern_words else bag.append(0)

  # La sortie est '0' pour chaque étiquette et '1' pour l'étiquette en cours (pour chaque motif)
  output_row = list(output_empty)
  output_row[classes.index(doc[1])] = 1

  training.append([bag, output_row])
# Mélange les caractéristiques et génère np.array
random.shuffle(training)
training = np.array(training)
# Crée entrainement (train) et teste les listes. X : motifs, Y : intentions
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")

# Créer modèle à 3 couches : 123 neurones dans la première, 64 dans la seconde, ?? dans la troisième
# Egal au nombre d'intentions pour prédire l'intention de sortie avec softmax
model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))

# Compiler le modèle. "Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model"
sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

# Ajuste (fitting) et sauvegarde le modèle
hist = model.fit(np.array(train_x), np.array(train_y), epochs = 200, batch_size = 5, verbose = 1)
model.save('chatbot_model.h5', hist)

print("model created")