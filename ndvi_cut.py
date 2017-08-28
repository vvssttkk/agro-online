#!/usr/bin/env python
"""
author: Trokhymenko Viktor
e-mail: trokhymenkoviktor@gmail.com
program: ndvi_maker
version: 1.0
data: 05/2017
"""

#to excec
#scenario/ndvi_cut.py pwd

import sys
import os #https://pythonworld.ru/moduli/modul-os.html http://pythoner.name/file-system  
import glob #list all files of a directory
from osgeo import gdal
import json,io
from pprint import pprint
import numpy as np

import other_moduls as om
#https://wombat.org.ua/AByteOfPython/first_steps.html



def copy_ndvi_rgb(satellite,pwd):
    if satellite=='S2A':
        os.chdir('{}'.format(glob.glob('L1C*')[0]))
        os.chdir('IMG_DATA');   

        cmd_ndvi='cp {} {}'.format(glob.glob('*_NDVI.TIF')[0], pwd)    
        os.system(cmd_ndvi)
        cmd_rgb='cp {} {}'.format(glob.glob('*_RGB.TIF')[0], pwd)    
        os.system(cmd_rgb)        

        os.chdir('..')
        os.chdir('..')
    elif satellite=='LC08':
        os.chdir('{}'.format(glob.glob('LC08*')[0]))
        
        cmd_ndvi='cp {} {}'.format(glob.glob('*_NDVI.TIF')[0], pwd)    
        os.system(cmd_ndvi)
        cmd_rgb='cp {} {}'.format(glob.glob('*_RGB.TIF')[0], pwd)    
        os.system(cmd_rgb) 

        os.chdir('..')    
    else:
        print 'Error copy ndvi & rgb'


def find_utm(satellite):
    if satellite=='S2A':
        gdalData=gdal.Open('{}'.format(glob.glob('*_NDVI.TIF')[0]))
        getproj=gdalData.GetProjection()
        utm=getproj[26:28]    
        
    elif satellite=='LC08':
        gdalData=gdal.Open('{}'.format(glob.glob('*_NDVI.TIF')[0]))
        getproj=gdalData.GetProjection()
        utm=getproj[26:28]    
        
    return utm


#------------------------------------------------------------
if __name__ == '__main__':
	pwd=sys.argv[1]
	os.chdir(sys.argv[1])
	system_dir = '/home/admin-pc/scenario/'
	
	#-------------------------------
	#farm identification & satellite 
	farm=glob.glob('*.json')[0]
	farm=farm[:2]

	if glob.glob('LC08*'):
	    satellite='LC08'
	    #folder_satellite=glob.glob('LC8*')[0]
	elif glob.glob('L1C*'):
	    satellite='S2A'
	    #folder_satellite=glob.glob('L1C*')[0]
	else:
	    print 'No satellite data directory'
	#-------------------------------

	#-------------------------------
	#copy ndvi & rgb in pwd
	copy_ndvi_rgb(satellite,pwd)

	#find utm reading NDVI.TIF
	utm=find_utm(satellite)
	srs='+proj=utm +zone={} +datum=WGS84 +units=m +no_defs'.format(utm)

	#conversion & searchCoordinates 
	#ll1,ll2,ur1,ur2=om.Conversion_searchCoordinates(farm,utm,pwd)
	ll1,ll2,ur1,ur2=om.Conversion_searchCoordinates_new(farm,utm,pwd)
	#-------------------------------

	#-------------------------------
	#sclicing shp-file
	os.mkdir('result')

	farm4cut='{}.json'.format(farm)
	with open(farm4cut) as data_file:    
	    jsonFile = json.load(data_file)

	for gg in jsonFile['features']:   
	    with io.open('result/{}.json'.format(gg['properties']['id']), 'w') as outfile:
	        str_ = json.dumps(gg,ensure_ascii=False)
	        outfile.write(str_)
	    
	    cmd_json2shap='ogr2ogr -F "ESRI Shapefile" result/{}.shp result/{}.json OGRGeoJSON'.format(gg['properties']['id'],gg['properties']['id'])
	    os.system(cmd_json2shap)
	#-------------------------------

	#-------------------------------
	#repeated tile sclicing NDVI + RGB with a difference of 5 meters
	cmd_warp0_ndvi='gdalwarp -te {} {} {} {} -tr 5 5 {} {}_cuted.TIF'.format(ll1,ll2,ur1,ur2,glob.glob('*_NDVI.TIF')[0],glob.glob('*_NDVI.TIF')[0][:len(glob.glob('*_NDVI.TIF')[0])-4])
	os.system(cmd_warp0_ndvi)
	cmd_warp0_rgb='gdalwarp -te {} {} {} {} -tr 5 5 {} {}_cuted.TIF'.format(ll1,ll2,ur1,ur2,glob.glob('*_RGB.TIF')[0],glob.glob('*_RGB.TIF')[0][:len(glob.glob('*_RGB.TIF')[0])-4])
	os.system(cmd_warp0_rgb)

	#redrawing the rasters in the GeoJSON projection
	cmd_warp1_ndvi='gdalwarp -t_srs "+proj=longlat +datum=WGS84 +no_defs" {} {}_cuted_proj.TIF'.format(glob.glob('*_NDVI_cuted.TIF')[0],glob.glob('*_NDVI_cuted.TIF')[0][:len(glob.glob('*_NDVI_cuted.TIF')[0])-10])
	os.system(cmd_warp1_ndvi)
	cmd_warp1_rgb='gdalwarp -t_srs "+proj=longlat +datum=WGS84 +no_defs" {} {}_cuted_proj.TIF'.format(glob.glob('*_RGB_cuted.TIF')[0],glob.glob('*_RGB_cuted.TIF')[0][:len(glob.glob('*_RGB_cuted.TIF')[0])-10])
	os.system(cmd_warp1_rgb)

	#del & rename
	cmd_rename_ndvi_del='rm {} {}'.format(glob.glob('*_NDVI.TIF')[0],glob.glob('*_NDVI_cuted.TIF')[0])
	os.system(cmd_rename_ndvi_del)
	cmd_rename_ndvi='mv {} {}.TIF'.format(glob.glob('*_NDVI_cuted_proj.TIF')[0],glob.glob('*_NDVI_cuted_proj.TIF')[0][:len(glob.glob('*_NDVI_cuted_proj.TIF')[0])-15])
	os.system(cmd_rename_ndvi)

	cmd_rename_rgb_del='rm {} {}'.format(glob.glob('*_RGB.TIF')[0],glob.glob('*_RGB_cuted.TIF')[0])
	os.system(cmd_rename_rgb_del)
	cmd_rename_rgb='mv {} {}.TIF'.format(glob.glob('*_RGB_cuted_proj.TIF')[0],glob.glob('*_RGB_cuted_proj.TIF')[0][:len(glob.glob('*_RGB_cuted_proj.TIF')[0])-15])
	os.system(cmd_rename_rgb)
	#-------------------------------

	#-------------------------------
	#sclicing tif-files & conver2png
	bla=glob.glob('*_NDVI.TIF')[0]

	for gg in jsonFile['features']: 	    
	    if satellite=='S2A':
	        NDVI_FName='result/{}{}{}_{}_NDVI_P20160317_S2A.TIF'.format(bla[13:15],bla[11:13],bla[7:11],gg['properties']['id'])
	        RGB_FName='result/{}{}{}_{}_RGB_S2A.TIF'.format(bla[13:15],bla[11:13],bla[7:11],gg['properties']['id'])

	        cmd_sys_arg_ndvi='gdalwarp -dstnodata 0 -q -cutline result/{}.shp -crop_to_cutline -of GTiff {} {}'.format(gg['properties']['id'],glob.glob('*_NDVI.TIF')[0],NDVI_FName)
	        os.system(cmd_sys_arg_ndvi)

	        cmd_sys_arg_rgb='gdalwarp -dstnodata 0 -q -cutline result/{}.shp -crop_to_cutline -of GTiff {} {}'.format(gg['properties']['id'],glob.glob('*_RGB.TIF')[0],RGB_FName)
	        os.system(cmd_sys_arg_rgb)

	        cmd_lut_cm='python {}add_lut.py {}cm2.lut {}'.format(system_dir,system_dir,NDVI_FName)
	        os.system(cmd_lut_cm)


	        cmd_conv_png_ndvi='gdal_translate -of PNG {} result/{}{}{}_{}_NDVI_P20160317_S2A.PNG'.format(NDVI_FName,bla[13:15],bla[11:13],bla[7:11],gg['properties']['id'])
	        os.system(cmd_conv_png_ndvi)

	        cmd_conv_png_rgb='gdal_translate -of PNG {} result/{}{}{}_{}_RGB_S2A.PNG'.format(RGB_FName,bla[13:15],bla[11:13],bla[7:11],gg['properties']['id'])
	        os.system(cmd_conv_png_rgb)

	       	#getMetaData
	       	png='{}{}{}_{}_NDVI_P20160317_S2A.PNG'.format(bla[13:15],bla[11:13],bla[7:11],gg['properties']['id'])
	       	nameFarm=gg['properties']['id']
	       	om.getMetaData(png,nameFarm,pwd)
	    
	    elif satellite=='LC08': ##http://calendarin.net/ru/day-number-in-year
	        tayl=glob.glob('*_NDVI.TIF')[0]                
	        
	        NDVI_FName='result/{}{}{}_{}_NDVI_P20160317_LC8.TIF'.format(bla[23:25],bla[21:23],bla[17:21],gg['properties']['id'])
	        RGB_FName='result/{}{}{}_{}_RGB_LC8.TIF'.format(bla[23:25],bla[21:23],bla[17:21],gg['properties']['id'])  
	        
	        cmd_sys_arg_ndvi='gdalwarp -dstnodata 0 -q -cutline result/{}.shp -crop_to_cutline -of GTiff {} {}'.format(gg['properties']['id'],glob.glob('*_NDVI.TIF')[0],NDVI_FName)
	        os.system(cmd_sys_arg_ndvi)

	        cmd_sys_arg_rgb='gdalwarp -dstnodata 0 -q -cutline result/{}.shp -crop_to_cutline -of GTiff {} {}'.format(gg['properties']['id'],glob.glob('*_RGB.TIF')[0],RGB_FName)
	        os.system(cmd_sys_arg_rgb)
	        
	        cmd_lut_cm='python {}add_lut.py {}cm2.lut {}'.format(system_dir,system_dir,NDVI_FName)
	        os.system(cmd_lut_cm)

	        
	        cmd_conv_png_ndvi='gdal_translate -of PNG {} result/{}{}{}_{}_NDVI_P20160317_S2A.PNG'.format(NDVI_FName,bla[23:25],bla[21:23],bla[17:21],gg['properties']['id'])
	        os.system(cmd_conv_png_ndvi)

	        cmd_conv_png_rgb='gdal_translate -of PNG {} result/{}{}{}_{}_RGB_S2A.PNG'.format(RGB_FName,bla[23:25],bla[21:23],bla[17:21],gg['properties']['id'])
	        os.system(cmd_conv_png_rgb)

	        #getMetaData
	       	png='{}{}{}_{}_NDVI_P20160317_S2A.PNG'.format(bla[23:25],bla[21:23],bla[17:21],gg['properties']['id'])
	       	nameFarm=gg['properties']['id']
	       	om.getMetaData(png,nameFarm,pwd)
	    
	    os.system('rm result/{}.json'.format(gg['properties']['id']))    
	#cdm_del='rm *.TIF result/*.dbf result/*.json result/*.prj result/*.shp result/*.shx result/*.TIF result/*.xml'
	cdm_del='rm *.TIF result/*.dbf result/*.prj result/*.shp result/*.shx result/*.TIF result/*.xml'
	os.system(cdm_del)
	print '='*20
	print 'cuting done!'
	print '='*20
	#-------------------------------