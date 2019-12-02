#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:35:50 2019

@author: nicolas
"""
import numpy as np
X = np.load('sentinel2_3a_20180815.npy')

def standardize_band(img):
    amax = np.max(img)
    img = img/amax
    return img

def plot_image(array,blue=0,green=1,red=2,save_as=False):
    
    b_channel = standardize_band(array[:,:,blue])
    g_channel = standardize_band(array[:,:,green])
    r_channel = standardize_band(array[:,:,red])
    
    normalized_image = np.stack([r_channel, g_channel, b_channel], axis=-1)
    

    plt.imshow(normalized_image)

plot_image(X)



ndvi = np.zeros([200,200],dtype=np.float)

