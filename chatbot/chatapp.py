#!/usr/bin/env python3
# coding: utf8
"""
Nom: chatapp.py
Rôle: Interface graphique utilisateur. Récupère les demandes de l'utilsateur, en prédit la classe grâce au modèle chatbot_model.h5 et enfin affiche une des réponses possible pour la classe.
Auteur: Robin Clerc robin.clerc@gmail.com
Version: 1.0
Date: 25/08/2021
Licence: GPLv3.0
Usage: python3 chatapp.py
Autres: Dans le cadre du cours P8 IED L1 IF UOR par P. Kislin
https://data-flair.training/blogs/python-chatbot-project/
https://www.datacorner.fr/nltk/
https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
"""

# Importer paquets et fichiers pickle générés pendant l'entraînement
import nltk
#from nltk.stem import WordNetLemmatizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
#lemmatizer = WordNetLemmatizer()
lemmatizer = FrenchLefffLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Nettoyer et présenter l'entrée utilisateur
def clean_up_sentence(sentence):
  # Convertis le motif en jeton - sépare les mots en tableau
  sentence_words = nltk.word_tokenize(sentence, language="french")
  # Lemmatise chaque mot
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words
  
# Retourne tableau de groupe (bag) de mots : 0 ou 1 si le mot existe dans la phrase
def bow(sentence, words, show_details = True):
  # Converti le motif en jetton
  sentence_words = clean_up_sentence(sentence)
  # Groupe (bag) de mots - matrice de N mots, vocabulaire
  bag = [0] * len(words)
  for s in sentence_words:
    for i, w in enumerate(words):
      if w == s:
        # Assigne 1 si le mot est en position vocabulaire
        bag[i] = 1
        if show_details:
          print("found in bag: %s" % w)
  return (np.array(bag))

def predict_class(sentence, model):
  # Filtre les prédictions inférieures à un seuil
  p = bow(sentence, words, show_details = False)
  res = model.predict(np.array([p]))[0]
  ERROR_THRESHOLD = 0.25
  results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
  # Trie par probabilité décroissante
  results.sort(key = lambda x: x[1], reverse = True)
  return_list = []
  for r in results:
    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Réponse en fonction de la classe
def getResponse(ints, intents_json):
  tag = ints[0]['intent']
  list_of_intents = intents_json['intents']
  for i in list_of_intents:
    if (i['tag'] == tag):
      result = random.choice(i['responses'])
      break
  return result

def chatbot_response(text):
  ints = predict_class(text, model)
  res = getResponse(ints, intents)
  return res

# Interface graphique utilisateur (GUI) avec Tkinter
import tkinter
from tkinter import *

def send():
  msg = EntryBox.get("1.0", 'end-1c').strip()
  EntryBox.delete("0.0",END)

  if msg != '':
    ChatLog.config(state = NORMAL)
    ChatLog.insert(END, "Humain: " + msg + '\n\n')
    ChatLog.config(foreground = "#442265", font = ("Verdana", 12))

    res = chatbot_response(msg)
    ChatLog.insert(END, "Bot: " + res + '\n\n')

    ChatLog.config(state = DISABLED)
    ChatLog.yview(END)

if __name__ == '__main__':

  base = Tk()
  base.title("UOR ex.7.2 - Chatbot")
  base.geometry("400x500")
  base.resizable(width = FALSE, height = FALSE)

  # Créer la fenêtre de chat
  ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial")

  ChatLog.config(state=DISABLED)

  # Barre de défilement dans la fenêtre de chat
  scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="hand2")
  ChatLog['yscrollcommand'] = scrollbar.set

  # Créer bouton envoyer message
  SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Envoyer", width="12", height="5", bd="0", bg="#32de97", activebackground="#3c9d9b", fg="#ffffff", command=send, cursor="heart")

  # Créer champs où écrire le message
  EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")
  #EntryBox.bind("<Return>", send)

  # Placement absolu des différents éléments de GUI
  scrollbar.place(x=376, y=6, height=386)
  ChatLog.place(x=6, y=6, height=386, width=370)
  EntryBox.place(x=128, y=401, height=90, width=265)
  SendButton.place(x=6, y=401, height=90)

  base.mainloop()