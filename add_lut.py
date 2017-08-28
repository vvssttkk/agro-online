import time
from osgeo import gdal
import sys
import numpy

LUT_ENTRIES = 256

def read_lut(lut_fn):
    lut = numpy.loadtxt(lut_fn)
    assert len(lut) >= LUT_ENTRIES
    assert lut.shape[1] >= 4

    return lut

def process(lut_fn, data_fn):
    lut = read_lut(lut_fn)
    in_dataset = gdal.Open(data_fn, gdal.GF_Write)

    band = in_dataset.GetRasterBand(1)
    colortable = gdal.ColorTable()

    for i, entry in enumerate(lut[:LUT_ENTRIES]):
        entry = tuple(int(max(0,min(255,255*u))) for u in entry)
        colortable.SetColorEntry(i, entry)

    band.SetColorTable(colortable)

    in_dataset.FlushCache()
    del in_dataset

def printUsage():
    print "add_lut.py <lut-file> <srcFile>"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        printUsage()
        sys.exit(1)

    start = time.time()

    lut_fn = sys.argv[1]
    data_fn = sys.argv[2]

    process(lut_fn, data_fn)

    finish = time.time()
