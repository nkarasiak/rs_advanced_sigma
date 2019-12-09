#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 08:35:42 2019

@author: nkarasia
"""
import numpy as np
import gdal

def lire_image(in_image):
    """
    Fonction qui retourne un objet gdal de l'image demandée
    
    Parameters
    -----------
    in_image : str
        Path to the desired raster image.
        
    Returns
    --------
    gdal_object
        gdal_object corresponding to in_image.
    """
    data_src = gdal.Open(in_image)
    
    if data_src is None:
        raise ReferenceError("Sorry coco, mais ton image {0} n'existe pas.".format(in_image)) 
    else:
        print('Bo/belle gosse')
    return data_src

def calcul_ndvi(red,infrared):
    """
    Fonction qui calcule le NDVI à partir de deux tableaux
    
    Parameters
    -----------
    red : np.ndarray
        array of 2 dimensions corresponding to the red band
    infrared : np.ndarray
        array of 2 dimensions corresponding to the infrared band
        
    Returns
    ---------
    ndvi : np.ndarray
        Array of 2 dimensions
        
    """
    ndvi = np.divide((infrared-red),(infrared+red.astype(np.float)))
    
    return ndvi

def ecrire_image(objet_gdal,tableau,out_image):
    """
    Fonction qui permet d'écrire une image à partir d'un tableau et d'un objet gdal.
    
    Parameters
    -----------
    objet_gdal : gdal
        objet gdal servant à :
            - copier la taille de l'image
            - copier la projection
            - copier la transformation
    tableau : np.ndarray
        tableau gdal à écrire
    out_image : str
        chemin de l'image à écrire au format geotiff (extension '.tif')
    """
    
    driver = gdal.GetDriverByName("GTiff") # on choisi de créer un GeoTIFF
    out_data = driver.Create(out_image, objet_gdal.RasterXSize, objet_gdal.RasterYSize, 1, gdal.GDT_Float32) # 1 pour une bande
    out_data.SetProjection(objet_gdal.GetProjection()) # même projection que l'image d'origine
    out_data.SetGeoTransform(objet_gdal.GetGeoTransform()) # même géotransformation que l'image d'origine
    
    out_data.GetRasterBand(1).WriteArray(tableau) # j'écris mon NDVI dans la bande 1
    out_data.FlushCache() # écrit sur le disque
    out_data = None
    
if __name__ == '__main__':
#    toto = lire_image('toto.tif')
    
    sentinel2 = lire_image('rs_advanced_sigma-data/sentinel2_3a_20180815.tif')

    red = sentinel2.GetRasterBand(3).ReadAsArray()
    infrared = sentinel2.GetRasterBand(4).ReadAsArray()
    
    ndvi = calcul_ndvi(red,infrared)    
    
    ecrire_image(objet_gdal = sentinel2,tableau = ndvi,out_image = '/tmp/ndvi.tif')
    