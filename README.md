# agro-online

in this repository you can find how calculate biomace activity - ndvi (Normalized Difference Vegetation Index) using satellite landsat8 (https://landsat.gsfc.nasa.gov/landsat-data-continuity-mission/) & sentinel-2 (https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

the sequence run files:
1. download some snapshot from
      * to lc8 https://earthexplorer.usgs.gov
      * to s2a https://scihub.copernicus.eu/dhus/#/home
2. run _downloadFarm.py_ to download some farm
3. run _ndvi_maker.py_ to doing _ndvi.tif & _rgb.tif
4. run _ndvi_cut.py_ to cutting _ndvi.tif & _rgb.tif for farm

