#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:40:29 2019

@author: nkarasia
"""
import museotoolbox as mtb

# J'importe les données de test de museotoolbox

raster,vector = mtb.datasets.load_historical_data()
X,y,g = mtb.processing.extract_ROI(raster,vector,'Class','uniquefid')

# je choisis mon algorithme
from sklearn.ensemble import RandomForestClassifier
# je fixe les meilleures paramètres à trouver.
# Ici je dis de choisir entre 10 et 100 arbres
parameters = dict(n_estimators=[10,100]) #  nombre d'arbres de l'algorithme : 10 et 100

# je sélectionne la validation croisée qui laisse un polygone de côté pour la validation
losgo = mtb.cross_validation.LeaveOneSubGroupOut()

# j'importe la classe sklearn qui permet de m'entrainer avec une grille de recherche

from sklearn.model_selection import GridSearchCV
# je définis ma grille de recherche avec ma validation croisée
model = GridSearchCV(RandomForestClassifier(),parameters,cv=losgo)
# j'entraine le modèle
model.fit(X,y,g)

print('Accord global issu de la validation croisée : '+str(model.best_score_))

## Je prédis mon raster
rM = mtb.processing.RasterMath(raster)
rM.add_function(model.predict,out_image='/tmp/ma_classification.tif')
rM.run()
