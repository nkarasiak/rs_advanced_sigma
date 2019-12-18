#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:25:08 2019

@author: nkarasia
"""
import numpy as np
from sklearn.datasets import load_iris

X,y = load_iris(return_X_y=True)
X.shape
y.shape #

y[0] # label du premier individu

X[0,...] # toutes les variables du premier individu

X[0,[1,3]] # la largeur du sépal et du pétal du premir individu

from sklearn.tree import DecisionTreeClassifier

nelly = DecisionTreeClassifier()

nelly.fit(X,y) # nelly apprend le modèle

y_pred = nelly.predict(X) # nelly prédit les variables qu'elle a déjà vu

from sklearn.metrics import accuracy_score

oa = accuracy_score(y,y_pred) # on évalue la prédiction de nelly
print(oa)

### WOMAN IN BLACK
### nelly oublie tout

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

np.unique(y_train,return_counts=True) # combien d'individus par espèce

nelly = DecisionTreeClassifier()

nelly.fit(X_train,y_train) # nelly apprend avec le jeu d'entraiment
# nelly n'a pas connaissance du jeu de validation
# vous écrivez vraiment tout ?
# c'est un test
# il ne vaut mieux pas écrire ces lignes
# de toute façon le code sera sur le git

y_pred = nelly.predict(X_test) # prédit à partir des longueurs/largeurs des pétales/sépales

oa = accuracy_score(y_test,y_pred)

from sklearn.metrics import confusion_matrix
#np.unique(y_test,return_counts=True)
matrice = confusion_matrix(y_test,y_pred)
print(matrice)

labels=['Iris-Setosa','Iris-Versicolour','Iris-Virginica']

from museotoolbox import charts
cm = charts.PlotConfusionMatrix(matrice,cmap='Purples')
cm.add_text()
#cm.color_diagonal('Reds')
cm.add_x_labels(labels)
cm.add_y_labels(labels)
#cm.add_accuracy()
cm.add_f1()