#from IPython import get_ipython
#get_ipython().magic('reset -sf')

#from jdcal import gcal2jd
#from latlon_tool import lonto180
import os
import shutil

#file = "masie_all_r00_v01_2017155_4km.tif"


def plot_ice_extent(filename,in_path,tools_path):
    from read_ims_extent_latlon import read_ims_extent_latlon
    from PIL import Image
    import matplotlib

    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')

    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    import numpy as np

    #read ice extent latlon --------------------
    region = [-40, 100, 68, 87] #[left, right, bottom, top]
    region = np.asarray(region)
    nx = 6144
    ny = 6144
    
    slatlon = read_ims_extent_latlon(tools_path)
    slat = slatlon[0][:]
    slon = slatlon[1][:]
    
    vec_slat = np.reshape(slat,nx*ny, order='C')
    vec_slon = np.reshape(slon,nx*ny, order='C')
    
    ii = np.where( (vec_slat >= region[2]) & (vec_slat <=region[3]) )
    
    vec_slon=((vec_slon+180)%360)-180
    
    #read ice extent file
    #extent = plt.imread(path + file)
    extent = np.asarray(Image.open(in_path + filename))
    vec_extent = np.reshape(extent,nx*ny,order='F')
    
    vec_slat_region = vec_slat[ii]
    vec_slon_region = vec_slon[ii]
    vec_extent_region = vec_extent[ii]
    
    #set basemap ------
    plt.figure(figsize=(10,6),dpi=300)
    
    map = Basemap(projection='merc',llcrnrlat=65,urcrnrlat=82,\
            llcrnrlon=-30,urcrnrlon=60,lat_ts=70,resolution='h')
    #map = Basemap(projection='stere', lon_0=clon, lat_0=clat, lat_ts=clat, \
    #               width=1800000,height=1100000, resolution='l')
    
    map.drawcoastlines()
    
    #missing=0, ocean=1, land=2, sea ice=3, coast line=4
    ow_ind = np.where(vec_extent_region == 3)
    
    slon_ow = vec_slon_region[ow_ind]
    slat_ow = vec_slat_region[ow_ind]
    
    x_ow, y_ow = map(slon_ow,slat_ow)
    
    map.scatter(x_ow,y_ow,color='white', s=5, marker='.')
    #map.pcolor(x_ow,y_ow,color='white',size=1,marker='.')
    
    map.drawparallels(np.arange(-80.,81.,10.))
    map.drawmeridians(np.arange(-180.,181.,10.))
    map.drawmapboundary(fill_color='white')
    map.fillcontinents(color='green',lake_color='aqua')
    
    plt.savefig(filename[0:29]+'.png', facecolor='gray', transparent='50', 
            bbox_inches='tight', pad_inches=0)









