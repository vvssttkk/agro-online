#!/usr/bin/env python
"""
author: Trokhymenko Viktor
e-mail: trokhymenkoviktor@gmail.com
program: downloadFarm
version: 0.1
data: 05/2017
"""

import sys
from grab import Grab

#to excec
#scenario/downloadFarm.py nameFarm pwd

farm=sys.argv[1]
pwd=sys.argv[2]

g = Grab()
g.setup(connect_timeout=60, timeout=90)
g.go("http://agro-online.com.ua/ru/auth/login/")
g.doc.set_input('email', 'demo@agro-online.com.ua')
g.doc.set_input('password', 'demo2016')
g.doc.submit()
g.go('http://agro-online.com.ua/export/satellite/fields/?key=FSKi1A23tC3ROh3sSY5y1tFSKiAtC314ROh143AtC3R49w&amp;company='+farm+'&amp;private=1')

f = open('{}/{}.json'.format(pwd,farm),'w')
f.write(g.doc.select('//*').text())
f.close()

print 'farm download'

#if (len(sys.argv) == 3):

#else:
 #   print "\tYou must have 2 argv!"
 #   print "\texample: python GetJson.py 10 output_filename.json"