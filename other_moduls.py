#!/usr/bin/env python2
"""
Author: Trokhymenko Viktor
E-mail: trokhymenkoviktor@gmail.com
Program: other_moduls
Version: 0.2
Data: 05/2017
"""

from osgeo import gdal
import json
import os
import numpy as np

def Conversion_searchCoordinates(farm,utm,pwd):
    os.chdir(pwd)

    #Conversion
    #json->shp
    cmd1='ogr2ogr -F "ESRI Shapefile" {}.shp {}.json OGRGeoJSON'.format(farm,farm)
    os.system(cmd1)
    
    #SHP (WGS84) -> SHP(UTM **)
    cmd2='ogr2ogr -a_srs "+proj=longlat +datum=WGS84 +no_defs" -t_srs "+proj=utm +zone={} +datum=WGS84 +units=m +no_defs" {}-UTM-{}.shp {}.shp'.format(utm,farm,utm,farm)
    os.system(cmd2)
    
    #SHP(UTM **) -> JSON
    cmd3='ogr2ogr -F GeoJSON {}-UTM-{}.json {}-UTM-{}.shp'.format(farm,utm,farm,utm)
    os.system(cmd3)
    
    #delete unnecessary files
    # for windows
    cmd4='rm {}.dbf {}.prj {}.shp {}.shx {}-UTM-{}.dbf {}-UTM-{}.prj {}-UTM-{}.shp {}-UTM-{}.shx'.format(farm,farm,farm,farm,farm,utm,farm,utm,farm,utm,farm,utm)
    os.system(cmd4)
    
    print 'conversion done!\n'
    
    #-----------------
    #searchCoordinates
    farm_utm='{}-UTM-{}.json'.format(farm,utm)
    print farm_utm
    
    with open(farm_utm) as data_file:    
        jsonFile = json.load(data_file)
    
    LL=[]#np.array([])
    UR=[]#np.array([])
    
    i=0
    for gg in jsonFile['features']:       
        LL.append(gg['geometry']['coordinates'])
        UR.append(gg['geometry']['coordinates'])
        i+=1
    
    print 'lens = %s' % i
    
    #search ll
    ll=min(min(min(LL)))       
    ll1= int(ll[0])
    ll2= int(ll[1])    
    ll1-=7000
    ll2-=7000
    while(ll1%30!=0):
        ll1-=1
    while(ll2%30!=0):
        ll2-=1
    print('ll: [ {} ; {} ]').format(ll1,ll2)
    
    #search ur
    ur=max(max(max(UR)))
    ur1= int(ur[0])
    ur2= int(ur[1])
    ur1+=7000
    ur2+=7000
    while(ur1%30!=0):
        ur1+=1 
    while(ur2%30!=0):
        ur2+=1 
    print('ur: [ {} ; {} ]').format(ur1,ur2)
    
    #delete *-UTM_*.json
    cmd_5='rm {}-UTM-{}.json'.format(farm,utm)
    os.system(cmd_5)
    
    print 'searchCoordinates done!'
    
    return ll1,ll2,ur1,ur2

def Conversion_searchCoordinates_new(farm,utm,pwd):
    os.chdir(pwd)

    #Conversion
    #json->shp
    cmd1='ogr2ogr -F "ESRI Shapefile" {}.shp {}.json OGRGeoJSON'.format(farm,farm)
    os.system(cmd1)
    
    #SHP (WGS84) -> SHP(UTM **)
    cmd2='ogr2ogr -a_srs "+proj=longlat +datum=WGS84 +no_defs" -t_srs "+proj=utm +zone={} +datum=WGS84 +units=m +no_defs" {}-UTM-{}.shp {}.shp'.format(utm,farm,utm,farm)
    os.system(cmd2)
    
    #SHP(UTM **) -> JSON
    cmd3='ogr2ogr -F GeoJSON {}-UTM-{}.json {}-UTM-{}.shp'.format(farm,utm,farm,utm)
    os.system(cmd3)
    
    #delete unnecessary files
    # for windows
    cmd4='rm {}.dbf {}.prj {}.shp {}.shx {}-UTM-{}.dbf {}-UTM-{}.prj {}-UTM-{}.shp {}-UTM-{}.shx'.format(farm,farm,farm,farm,farm,utm,farm,utm,farm,utm,farm,utm)
    os.system(cmd4)
    
    print 'conversion done!\n'
    
    #-----------------
    #searchCoordinates
    farm_utm='{}-UTM-{}.json'.format(farm,utm)
    print farm_utm
    
    with open(farm_utm) as data_file:    
        jsonFile = json.load(data_file)
    
    LL=[]#np.array([])
    UR=[]#np.array([])
    
    i=0
    for gg in jsonFile['features']:       
        LL.append(gg['geometry']['coordinates'])
        UR.append(gg['geometry']['coordinates'])
        i+=1
    
    print 'lens = %s' % i
    
    #search ll & ur
    
    ll1=int(min(min(min(LL)))[0])
    ll2=int(max(max(max(UR)))[1])
    ll1-=7000
    ll2-=7000
    while(ll1%30!=0):
        ll1-=1
    while(ll2%30!=0):
        ll2-=1
    print('ll: [ {} ; {} ]').format(ll1,ll2)
    
    #search ur
   
    ur1=int(max(max(max(UR)))[0])
    ur2=int(min(min(min(LL)))[1])
    ur1+=7000
    ur2+=7000
    while(ur1%30!=0):
        ur1+=1 
    while(ur2%30!=0):
        ur2+=1 
    print('ur: [ {} ; {} ]').format(ur1,ur2)
    
    #delete *-UTM_*.json
    cmd_5='rm {}-UTM-{}.json'.format(farm,utm)
    os.system(cmd_5)
    
    print 'searchCoordinates done!'
    
    return ll1,ll2,ur1,ur2

def getMetaData(png,nameFarm,pwd):
    print 'start getMetaData'
    os.chdir('{}/result'.format(pwd))
    print os.getcwd()

    getPNG = gdal.Open(png)
    tempPNG=getPNG.ReadAsArray()

    my_file = open('{}_meta.json'.format(png[0:32]), 'a')
    print 'my_file: ', my_file

    #cloud_coverage
    cloud_coverage=round((np.count_nonzero(tempPNG==255)+np.count_nonzero(tempPNG==254)))/np.count_nonzero(tempPNG)*10000/10000.
    #avg_ndvi
    avg_ndvi=0
    if (np.count_nonzero((tempPNG>30)&(tempPNG<77))!=0):
        avg_ndvi = avg_ndvi + 1.*np.count_nonzero((tempPNG>30)&(tempPNG<77))/np.count_nonzero((tempPNG>30)&(tempPNG<254))*tempPNG[(tempPNG>30)&(tempPNG<77)].sum()/np.count_nonzero((tempPNG>30)&(tempPNG<77))
    elif (np.count_nonzero((tempPNG>76)&(tempPNG<99))!=0):
        avg_ndvi = avg_ndvi + 1.*np.count_nonzero((tempPNG>76)&(tempPNG<99))/np.count_nonzero((tempPNG>30)&(tempPNG<254))*tempPNG[(tempPNG>76)&(tempPNG<99)].sum()/np.count_nonzero((tempPNG>76)&(tempPNG<99))  
    elif (np.count_nonzero((tempPNG>98)&(tempPNG<139)))!=0:
        avg_ndvi = avg_ndvi + 1.*np.count_nonzero((tempPNG>98)&(tempPNG<139))/np.count_nonzero((tempPNG>30)&(tempPNG<254))*tempPNG[(tempPNG>98)&(tempPNG<139)].sum()/np.count_nonzero((tempPNG>98)&(tempPNG<139))
    elif (np.count_nonzero((tempPNG>138)&(tempPNG<190))!=0):
        avg_ndvi = avg_ndvi + 1.*np.count_nonzero((tempPNG>138)&(tempPNG<190))/np.count_nonzero((tempPNG>30)&(tempPNG<254))*tempPNG[(tempPNG>138)&(tempPNG<190)].sum()/np.count_nonzero((tempPNG>138)&(tempPNG<190))
    elif (np.count_nonzero((tempPNG>189)&(tempPNG<254))!=0):
        avg_ndvi = avg_ndvi + 1.*np.count_nonzero((tempPNG>189)&(tempPNG<254))/np.count_nonzero((tempPNG>30)&(tempPNG<254))*tempPNG[(tempPNG>189)&(tempPNG<254)].sum()/np.count_nonzero((tempPNG>189)&(tempPNG<254))
    avg_ndvi=(avg_ndvi/255*10000)/10000.0
    #
    my_file.write('{\n')
    my_file.write('\t"id": "{}",'.format(nameFarm))
    my_file.write('\n\t"cloud_coverage": {},'.format(cloud_coverage))
    my_file.write('\n\t"avg_ndvi": {},'.format(avg_ndvi))
    #

    #snow_water
    snow_water=round(1.*np.count_nonzero((tempPNG>0)&(tempPNG<31))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.0
    #class1-5
    class_1=round(1.*np.count_nonzero((tempPNG>30)&(tempPNG<77))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    class_2=round(1.*np.count_nonzero((tempPNG>76)&(tempPNG<99))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    class_3=round(1.*np.count_nonzero((tempPNG>98)&(tempPNG<139))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    class_4=round(1.*np.count_nonzero((tempPNG>138)&(tempPNG<190))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    class_5=round(1.*np.count_nonzero((tempPNG>189)&(tempPNG<254))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.    
    #
    my_file.write('\n\t"by_class": {')
    my_file.write('\n\t\t"snow_water": {},'.format(snow_water))
    my_file.write('\n\t\t"class_1": {},'.format(class_1))
    my_file.write('\n\t\t"class_2": {},'.format(class_2))
    my_file.write('\n\t\t"class_3": {},'.format(class_3))
    my_file.write('\n\t\t"class_4": {},'.format(class_4))
    my_file.write('\n\t\t"class_5": {}'.format(class_5))
    my_file.write('\n\t}')
    #

    #palette
    p_005=round(1.*np.count_nonzero((tempPNG>0)&(tempPNG<14))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_020=round(1.*np.count_nonzero((tempPNG>13)&(tempPNG<52))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_030=round(1.*np.count_nonzero((tempPNG>51)&(tempPNG<78))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_035=round(1.*np.count_nonzero((tempPNG>77)&(tempPNG<90))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_040=round(1.*np.count_nonzero((tempPNG>89)&(tempPNG<103))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_045=round(1.*np.count_nonzero((tempPNG>102)&(tempPNG<116))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_050=round(1.*np.count_nonzero((tempPNG>115)&(tempPNG<129))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_055=round(1.*np.count_nonzero((tempPNG>128)&(tempPNG<141))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_060=round(1.*np.count_nonzero((tempPNG>140)&(tempPNG<153))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_065=round(1.*np.count_nonzero((tempPNG>152)&(tempPNG<167))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_070=round(1.*np.count_nonzero((tempPNG>166)&(tempPNG<180))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_075=round(1.*np.count_nonzero((tempPNG>179)&(tempPNG<192))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_080=round(1.*np.count_nonzero((tempPNG>191)&(tempPNG<205))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_085=round(1.*np.count_nonzero((tempPNG>204)&(tempPNG<218))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_090=round(1.*np.count_nonzero((tempPNG>217)&(tempPNG<231))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    p_100=round(1.*np.count_nonzero((tempPNG>230)&(tempPNG<253))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    #
    my_file.write('\n\t"by_palette": {')
    my_file.write('\n\t\t"p_005": {},'.format(p_005))
    my_file.write('\n\t\t"p_020": {},'.format(p_020))
    my_file.write('\n\t\t"p_030": {},'.format(p_030))
    my_file.write('\n\t\t"p_035": {},'.format(p_035))
    my_file.write('\n\t\t"p_040": {},'.format(p_040))
    my_file.write('\n\t\t"p_045": {},'.format(p_045))
    my_file.write('\n\t\t"p_050": {},'.format(p_050))
    my_file.write('\n\t\t"p_055": {},'.format(p_055))
    my_file.write('\n\t\t"p_060": {},'.format(p_060))
    my_file.write('\n\t\t"p_065": {},'.format(p_065))
    my_file.write('\n\t\t"p_070": {},'.format(p_070))
    my_file.write('\n\t\t"p_075": {},'.format(p_075))
    my_file.write('\n\t\t"p_080": {},'.format(p_080))
    my_file.write('\n\t\t"p_085": {},'.format(p_085))
    my_file.write('\n\t\t"p_090": {},'.format(p_090))
    my_file.write('\n\t\t"p_100": {}'.format(p_100))
    my_file.write('\n\t}')
    #

    #by_1_100
    my_file.write('\n\t"by_1_100": {')
    my_file.write('\n\t\t"1": {},'.format(round(1.*np.count_nonzero((tempPNG>=1)&(tempPNG<2))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.))
    my_file.write('\n\t\t"2": {},'.format(round(1.*np.count_nonzero((tempPNG>=2)&(tempPNG<5))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.))
    s=5
    p=0
    for i in range(3,101,2):
        my_file.write('\n\t\t"{}": {},'.format(i,round(1.*np.count_nonzero((tempPNG>=s)&(tempPNG<s+2))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.))
        my_file.write('\n\t\t"{}": {},'.format(i+1,round(1.*np.count_nonzero((tempPNG>=s+2)&(tempPNG<s+5))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.))
        s=s+5
        p = p + round(1.*np.count_nonzero((tempPNG>=s)&(tempPNG<s+2))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000. + round(1.*np.count_nonzero((tempPNG>=s+2)&(tempPNG<s+5))/np.count_nonzero((tempPNG>0)&(tempPNG<256))*10000)/10000.
    my_file.write('\n\t\t"control_summ": {}'.format(p))                      
    my_file.write('\n\t}')
    my_file.write('\n}')

    my_file.close()
    os.chdir(pwd)

    print '{}_meta.json done'.format(png[0:32])