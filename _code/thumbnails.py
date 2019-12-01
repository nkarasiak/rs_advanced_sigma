#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 09:50:51 2019

@author: nicolas
"""
import numpy as np
from matplotlib import pyplot as plt
import museotoolbox as mtb

in_image = "/mnt/DATA/Cours/Sigma/TLD/git_rs_advanced_sigma/data/sentinel2_3a_20180815.tif"
RM = mtb.geo_tools.RasterMath(in_image,return_3d=True,block_size=[1200,1200])

for block in RM.read_block_per_block():
    print(block)

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
    if save_as:        
        plt.savefig(save_as,bbox_inches='tight',dpi=300)
        
plot_image(block,save_as='/mnt/DATA/Cours/Sigma/TLD/git_rs_advanced_sigma/_images/s2_bouconne.jpg')


block_no_mask = np.copy(block)
plot_image(block_no_mask[300:600,300:600,:4],save_as='/mnt/DATA/Cours/Sigma/TLD/git_rs_advanced_sigma/_images/s2_bouconne_sample.jpg')

np.save('/mnt/DATA/Cours/Sigma/TLD/git_rs_advanced_sigma/data/sentinel2_3a_20180815.npy',block_no_mask[500:700,500:700,:4])

img = "/mnt/DATA/Cours/Sigma/TLD/git_rs_advanced_sigma/data/sentinel2_3a_20180815.npy"
X = np.load(img)
from matplotlib import pyplot as plt
plt.imshow((X[...,0])/(np.amax(X[...,0])),cmap='gray') 
