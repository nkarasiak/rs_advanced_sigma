#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:23:49 2019

@author: nicolas
"""
import numpy as np

def calcul_ndvi(array,red=2,infrared=3,method='slow'):
    """
    Fonction qui calcule le NDVI à partir d'un tableau
    
    Parameters
    -----------
    array : np array
        array of 3 dimensions
    red : int, optional (default=2)
        Position in the 3rd dimension of the red band
    infrared : int, optional (default=3)
        Position in the 3rd dimension of the infrared band
    method : str, optional (default='slow')
        If slow, will compute the NDVI pixel per pixel
        Else, will compute the NDVI by dividing the whole array.
    
    Returns
    ---------
    ndvi : np array
        Array of 2 dimensions
    """
    if method == 'slow':
        # parcours pixel par pixel
        ndvi = np.zeros([array.shape[0],array.shape[1]],dtype=float)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                ndvi[i,j] = (array[i,j,infrared] - array[i,j,red]) / (array[i,j,infrared] + np.float(array[i,j,red]))
    else:
        # calcul directement avec toute la bande
        ndvi = np.divide((array[...,infrared]-array[...,red]),array[...,infrared].astype(np.float)+array[...,red])
    return ndvi


if __name__ == '__main__':
    array = np.load('sentinel2_3a_20180815.npy')
    import time
    t0 = time.time()
    calcul_ndvi(array)
    t1 = time.time()
    print(t1-t0,'secondes')
    calcul_ndvi(array,method='a_fond_la_forme')
    print(time.time()-t1,'secondes')