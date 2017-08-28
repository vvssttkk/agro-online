# agro-online

in this repository you can find how calculate biomace index using satellite landsat8 & sentinel-2

1. download some snapshot from
      * to lc8 https://earthexplorer.usgs.gov
      * to s2a https://scihub.copernicus.eu/dhus/#/home
2. run _downloadFarm.py_ to download some farm from http://agro-online.com.ua/export/satellite/fields/?key=FSKi1A23tC3ROh3sSY5y1tFSKiAtC314ROh143AtC3R49w&amp;company='+farm+'&amp;private=1'     
3. run _ndvi_maker.py_ to doing ndvi.tif & rgb.tif
4. run _ndvi_cut.py_ to cutting ndvi.tif & rgb.tif for farm

