# -*- coding: utf-8 -*-
"""
Labwork Remote Sensing
MASTER SIGMA
@author: nkarasiak and mfauvel
"""
import numpy as np


def filter_array(in_array,grid_size=3,filter_type='mean'):
    """
    This function applies a filter on the image
    
    Input :
    --------
    in_array : array-like
        2 dimension (does not support more)
    grid_size : int
        Size of the square (odd size, 3,5,7...)    
    filter_type : str
        'mean','median','max', or 'min'
    
    Output : 
    --------
    out_array : array-like
        array of two dimension
    
    """
    availableTypes = ['min','max','amax','amin','mean','median']
    if filter_type not in availableTypes :
        raise Warning('Filter type `{}` is not available.\n\
                      Please use one of these types : {}'.format(filter_type,availableTypes))
            
    # import numpy function. (E.g. from numpy import median)
    filterFunction = getattr(__import__('numpy'),filter_type)
    
    s = int((grid_size-1)/2) # the number of neighbors (E.g (3-1)/2 = 1 neighbors)
    nl,nc = in_array.shape # get number of lines and columns from in_array
    out_array = np.empty([nl,nc],dtype=in_array.dtype) # create empty array with same shape  as arrayIn
    
    for i in range(nl): # begin with s size (to avoid 0)
        for j in range(nc):
            temp_i,temp_j = [i,j]
            if i<s:
                temp_i = s
            if j<s:
                temp_j = s
            
            view = in_array[temp_i-s:temp_i+1+s,temp_j-s:temp_j+1+s] # generate square
            out_array[i-s,j-s] = filterFunction(view) # filter the view and save it in arrayOut

    return out_array

if __name__ == "__main__" :

    in_array = np.load('/home/nicolas/Bureau/rs_advanced_sigma-data/sentinel2_3a_20180815.npy')
    
    filtered_array = np.zeros(in_array.shape)
    
    for band in range(in_array.shape[2]):
        filtered_array[:,:,band] = filter_array(in_array[:,:,band],grid_size=5)

    fig=plt.figure(figsize=(8, 8))
    fig.add_subplot(1,2,1)
    plt.title('original band')
    plt.imshow(in_array[...,3])
    fig.add_subplot(1,2,2)
    plt.title('smoothed band')
    plt.imshow(filtered_array[...,3])

        
        
