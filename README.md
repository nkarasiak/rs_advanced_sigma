Cours de télédétection avancée pour Master Sigma.
---
# Introduction

## Objectif

Ce cours a pour but de vous rendre le plus autonome possible en télédétection à partir de python. À la fin de ce cours vous serez capable d'interagir avec des images directement depuis python et ce de manière optimisée et efficiente (lecture par bloc par exemple). Vous allez aussi découvrir comment manier les algorithmes d'apprentissage automatique afin d'apprendre des modèles pour cartographier par l'exemple l'occupation du sol.

Les [données utilisées pour ce cours sont disponibles ici en ligne](https://github.com/nkarasiak/rs_advanced_sigma/archive/data.zip).

## Les bibliothèques python utilisées

Les bibliothèques python utilisées dans ce cours sont :
- gdal (raster)
- osr (projection)
- ogr (vecteur)
- numpy (tableau)
- scipy (calcul scientifique)
- scikit-learn (apprentissage automatique)
- museotoolbox (facilite la lecture/écriture des rasters)

Si une des bibliothèques venait à manquer, vous pouvez l'installer en tapant la commande suivante dans le terminal :
```bash
python3 -m pip install scikit-learn --user
```
## Le respect des conventions

Toutes les classes, fonctions et variables que nous allons créé pendant ce cours doivent suivre le convention PEP8.

| Type | Écriture |
|------|----------|
| Class | `MaSuperClasse` |
| Function | `ma_super_fonction` |
| Variable | `ma_variable` |

Les codes doivent être bien documentés, en suivant la [docstring numpy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html).

/!\ [Attention, un canard en plastique pourra venir relire et valider votre code](https://fr.wikipedia.org/wiki/M%C3%A9thode_du_canard_en_plastique).

## Planning

| Ordre | Date            | Horaire     | Thème                                                 |
|-------|-----------------|-------------|-------------------------------------------------------|
| 1     | Lun. 02/12/2019 | 8h/12h 	| Manipulation des tableaux/matrices.         		|
| 2     | Lun. 09/12/2019 | 8h/12h 	| Du tableau au raster. 				|
| 3     | Lun. 16/12/2019 | 13h30/17h30 | Filtre spatial (tenant compte des voisins)		|
| 4       | Ven. 18/12/2019 | 8h/12h      | Apprentissage automatique avec scikit-learn   	|
| 5     | Mer. 08/01/2020 | 8h/10h	| Découverte de Museo ToolBox                           |
| 6     | Ven. 08/01/2020 | 13h30/17h30 | PARTIEL                                               |

---

# Gestion des tableaux

Pour gérer un tableau ou une matrice (c'est-à-dire une image sans géoréférencement)

## Principe de numpy

### Ouvrir et connaître les informations principales

```python
import numpy as np
X = np.load('sentinel2_3a_20180815.npy')
X.shape # la taille de l'image (lignes, colonnes, bandes...)
>>> (200, 200, 4)
X.ndim # le nombre de dimensions
>>> 3
X.size # le nombre de cellules
>>> 160000
```

#### Exercice

- Comment pouvez-vous obtenir uniquement le nombre de lignes ?
- Comment pouvez-vous obtenir uniquement le nombre de bandes ?
- De combien de pixels est composée chaque bande ?

### Parcourir et afficher un tableau

Les `:` permettent de sélectionner toutes les cellules de la dimension en question.

Les `...` permettent de sélectionner toutes les dimensions suivantes ou précédentes.

```python
X[0,:,0] # première ligne, toutes les colonnes, première bande
X[0,...] # première ligne, et toutes les autres dimensions
X[...,0] # toutes les lignes et colonnes de la bande 0
```

```python
from matplotlib import pyplot as plt
plt.imshow((X[...,0])/(np.amax(X[...,0])),cmap='gray') # Si vous voulez afficher une bande
```

#### Exercice

- Accéder au pixel/ à la cellule de la première ligne et première colonne
- Accéder au pixel / à la cellule de la dernière ligne et dernière colonne
- Parcourir la matrice cellule par cellule (boucle for)
- Calculer le ndvi :
![\Large x=\frac{infrarouge-rouge}{infrarouge+rouge}](https://latex.codecogs.com/svg.latex?x=\frac{infrarouge-rouge}{infrarouge+rouge})

Sachant que l'infra-rouge est la dernière bande (la numéro 4, donc en partant de 0 la numéro 3, et le rouge est la bande numéro 3).

Pour ceux qui ont terminé, vous pouvez chronométrer et essayer d'optimiser le temps de traitement pour calculer le NDVI.

---

# D'une image au tableau

![Synthèse mensuelle de Sentinel-2 niveau 3A (Pôle Théia) sur la forêt de Bouconne en août 2018](_images/s2_bouconne.jpg)

## Lecture et ouverture d'une image

```python
import gdal
data_src = gdal.Open('sentinel2_3a_20180815.tif') # objet gdal
data_src.RasterCount  # nombre de bandes
data_src.RasterXSize  # nombre de colonnes
data_src.RasterYSize  # nombre de lignes

data_src.GetRasterBand(1) # renvoie le tableau de la bande 1
data_src.GetRasterBand(2) # renvoie le tableau de la bande 2

data_src.ReadAsArray() # renvoie toute l'image en tableau
```

### Exercice

- De combien de bandes, de lignes, et de colonnes est composée l'image ?
- Ouvrir l'image en objet gdal
- Calculer le NDVI pour toute l'image.
- Optimiser le calcul du NDVI pour ne plus le faire cellule par cellule (éviter la boucle for).

---

# Écriture d'une image géoréférencée

Maintenant que l'on sait ouvrir, lire, et faire un traitement sur une image, il ne reste plus qu'à sauvegarder le résultat dans une nouvelle image.

Pour cela quelques lignes pour définir nos besoins sont nécessaires :

```python
driver = gdal.GetDriverByName("GTiff") # on choisi de créer un GeoTIFF
out_data = driver.Create('/tmp/mon_ndvi.tif', data_src.RasterYSize, data_src.RasterXSize, 1, gdal.GDT_Float32) # 1 pour une bande
out_data.SetGeoTransform(data_src.GetGeoTransform()) # même géotransformation que l'image d'origine
out_data.SetProjection(data_src.GetProjection()) # même projection que l'image d'origine
```

La variable out_data est désormais une instance de votre fichier de sortie. Vous pouvez désormais intéragir avec cette instance et sauvegarder le résultat du ndvi dans votre nouvelle image :

```python
out_data.GetRasterBand(1).WriteArray(ndvi) # j'écris mon NDVI dans la bande 1
out_data.FlushCache() # écrit sur le disque
out_data = None # précaution, permet de bien spécifier que le fichier est fermé
```

## Exercice

Créer pour chacune consignes suivantes une fonction qui vous permet :
- de lire une image (fonction retournant l'objet gdal)
- de calculer le NDVI (à partir de l'objet gdal, on demande à l'utilisateur la position de la bande rouge et infrarouge)
- d'écrire une image (on donne un objet gdal, un tableau et le nom de fichier que l'on veut écrire)

Une fois terminée, vous pourrez à partir de 3 lignes :
- ouvrir une image
- calculer le ndvi
- écrire le ndvi

---

# Filtre spatial (tenant compte des voisins)

Comment identifier les forêts des cartes de l'État-Major ?
Des traits plus ou moins fins et plus ou moins serrés représentent les pentes dans les cartes. Nous avons donc besoin de supprimer ces rayures afind d'avoir une couleur verte homogène pour identifier la forêt.
![Fabas État-Major](_images/fabas.png)

Pour cela plusieurs filtres doivent être utilisés :
- closing filter (filtre de fermeture)
- médian (récupérer les contours)

## Exercice

- Quelle est la valeur des pixels blancs ?
- Quelle est la valeur des pixels noirs ?
- Que fait et à quoi sert le closing filter ?

![Illustration du closing filter](_images/closing.png)


Créer une fonction qui parcours l'image selon un nombre de voisins défini (1 = les premiers voisins (8 donc), 2 = les voisins jusqu'à 2 pixels de distance (24)...)
Puis en tenant compte des voisins, appliquez :
- un filtre max
- un filtre min
- un filtre median dont on peut définir le nombre d'itération

---

# Apprentissage automatique

Scikit-Learn

```python
import sklearn
```

---

# MuseoToolBox
