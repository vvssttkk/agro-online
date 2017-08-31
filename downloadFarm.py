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
g.go("http://mail.com/ru/auth/login/")
g.doc.set_input('email', 'email@mail.com')
g.doc.set_input('password', 'pass')
g.doc.submit()
g.go('http://mail.com/export/satellite/any='+farm+';private=1')

f = open('{}/{}.json'.format(pwd,farm),'w')
f.write(g.doc.select('//*').text())
f.close()

print 'farm download'
