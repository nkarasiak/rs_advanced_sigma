Cours de télédétection avancée pour Master Sigma.
---
# Introduction

## Objectif

Ce cours a pour but de vous rendre à la fois le plus autonome possible et le plus .

## Les bibliothèques python utilisées

Les bibliothèques python utilisées dans ce cours sont :
- gdal (raster)
- osr (projection)
- ogr (vecteur)
- numpy (tableau)
- scipy (calcul scientifique)
- scikit-learn (apprentissage automatique)
- museotoolbox (facilite la lecture/écriture des rasters)

## Le respect des conventions

Pep8

| Type | Écriture |
|------|----------|
| Class | `MaSuperClasse` |
| Function | `ma_super_fonction` |
| Variable | `ma_variable` |

## Planning

| Ordre | Date            | Horaire     | Thème                                                 |
|-------|-----------------|-------------|-------------------------------------------------------|
| 1     | Lun. 02/12/2019 | 8h/12h 	| Manipulation des tableaux/matrices.         		|
| 2     | Lun. 09/12/2019 | 8h/12h 	| Du tableau au raster. 				|
| 3     | Lun. 16/12/2019 | 13h30/17h30 | Filtre spatial (tenant compte des voisins)		|
| 4       | Ven. 18/12/2019 | 8h/12h      | Apprentissage automatique avec scikit-learn   	|
| 5     | Mer. 08/01/2020 | 8h/10h	| Découverte de Museo ToolBox                           |
| 6     | Ven. 08/01/2020 | 13h30/17h30 | PARTIEL                                               |

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

- Comment pouvez-vous obtenir que le nombre de lignes ?
- Comment pouvez-vous obtenir que le nombre de bandes ?
- De combien de pixels est composée chaque bande ?

### Parcourir et afficher un tableau

```python
X[0,:,0] # première ligne, toutes les colonnes, première bande
X[0,...] # première ligne, et toutes les autres dimensions
X[...,0] # toutes les lignes et colonnes de la bande 0
```

```python
from matplotlib import pyplot as plt
plt.imshow((X[...,0]+1)/(np.amax(X[...,0]+1)) # comme le NDVI va de -1 a 1, on standardise entre 0 et 1

#### Exercice

- Accéder au pixel/ à la cellule de la première ligne et première colonne

- Accéder au pixel / à la cellule de la dernière ligne et dernière colonne

- Parcourir la matrice cellule par cellule (boucle for)
- Calculer le ndvi :
![\Large x=\frac{infrarouge-rouge}{infrarouge+rouge}](https://latex.codecogs.com/svg.latex?x=\frac{infrarouge-rouge}{infrarouge+rouge})

Sachant que l'infra-rouge est la dernière bande (la numéro 4, donc en partant de 0 la numéro 3, et le rouge est la bande numéro 3)

Pour ceux qui ont fini, essayez d'optimiser le temps de traitement pour calculer le NDVI.

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


# Écriture d'une image géoréférencée

```python
driver = gdal.GetDriverByName("GTiff") # on choisi de créer un GeoTIFF
out_data = driver.Create('/tmp/mon_ndvi.tif', data_src.RasterYSize, data_src.RasterXSize, 1, gdal.GDT_Float32) # 1 pour une bande
out_data.SetGeoTransform(data_src.GetGeoTransform()) # même géotransformation que l'image d'origine
out_data.SetProjection(data_src.GetProjection()) # même projection que l'image d'origine
out_data.GetRasterBand(1).WriteArray(ndvi) # j'écris mon NDVI dans la bande 1
out_data.FlushCache()
```

#

#
