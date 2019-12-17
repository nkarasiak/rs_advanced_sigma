# -*- coding: utf-8 -*-
"""
Labwork Remote Sensing
MASTER SIGMA
@author: nkarasiak and mfauvel
"""
import gdal 
import numpy as np


def filter_array(in_array,grid_size=3,filter_type='mean'):
    """
    This function applies a filter on the image
    
    Parameters
    ----------
    in_array : np.ndarray
        2 dimension (does not support more)
    grid_size : int, optional (default=3)
        Size of the square (odd size, 3,5,7...)    
    filter_type : str, optional (default = 'mean')
        'mean','median','max', or 'min'
    
    Returns
    ---------
    out_array : np.ndarray
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
    if tableau.ndim<3 :
        tableau = tableau.reshape(-1,-1,1)
    
    n_bands = tableau.shape[-1]
    
    out_data = driver.Create(out_image, objet_gdal.RasterXSize, objet_gdal.RasterYSize, n_bands, gdal.GDT_Byte) # 1 pour une bande
    out_data.SetProjection(objet_gdal.GetProjection()) # même projection que l'image d'origine
    out_data.SetGeoTransform(objet_gdal.GetGeoTransform()) # même géotransformation que l'image d'origine
    
    for band in range(n_bands):
        out_data.GetRasterBand(band+1).WriteArray(tableau[...,band]) # j'écris chaque bande
        
    out_data.FlushCache() # écrit sur le disque
    out_data = None
    

def filter_historicalmap_process(array,grid_size=3):
    """
    Performs max, min, then median
    
    Parameters
    -----------
    array : np.ndarray
    
    Returns
    -------
    out_array : np.ndarray
        The array filtered with max, min, then median.
    """
    out_array = filter_array(array,grid_size=grid_size,filter_type='max')
    out_array = filter_array(out_array,grid_size=grid_size,filter_type='min')
    out_array = filter_array(out_array,grid_size=grid_size,filter_type='median')
    
    return out_array
    
def filter_per_band(gdal_object,grid_size=3):
    """
    Performs filter for each band
    
    Parameters
    -----------
    gdal_object : gdal_object
        The gdal object got from gdal.Open('image.tif')
    grid_size : int, optional (default=3)
        The size of the square to perform the spatial filter.
        
    Returns
    --------
    out_array : np.ndarray
        Array of same size as the input image, np.uint8.
    """
    # create empty table with same shape an gdal image
    out_array = np.empty((gdal_object.RasterYSize,gdal_object.RasterXSize,gdal_object.RasterCount),dtype=np.uint8)
    for band in range(gdal_object.RasterCount):
        band_array = gdal_object.GetRasterBand(band+1).ReadAsArray()
        out_array[...,band] = filter_historicalmap_process(band_array,grid_size=grid_size)
    return out_array
        
    
if __name__ == "__main__" :
    
    import lesson2
    
    # données à télécharger ici : https://github.com/lennepkade/HistoricalMap/archive/samples.zip
    image = 'rs_advanced_sigma-data/map.tif'
    
    data_src = lesson2.lire_image(image)
    
    filtered_image = filter_per_band(data_src,grid_size=3)
        
    ecrire_image(data_src,filtered_image,'/tmp/filtered_image.tif')
    
    import museotoolbox as mtb
    rM = mtb.processing.RasterMath(image,return_3d=True)
    rM.add_image('/tmp/filtered_image.tif')
    original,filtered =rM.get_block(24) # 

    
    from matplotlib import pyplot as plt
    fig=plt.figure(figsize=(8, 8))
    fig.add_subplot(1,2,1)
    plt.title('Image originale')
    plt.imshow(original)
    fig.add_subplot(1,2,2)
    plt.title('Image filtrée')
    plt.imshow(filtered)