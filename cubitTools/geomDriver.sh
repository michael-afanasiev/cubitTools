# /bin/sh

./generateGeom.py -t 6371 -b 6351 -d 1
./generateGeom.py -t 6351 -b 6319 -d 2
./generateGeom.py -t 6319 -b 6271 -d 3
./generateGeom.py -t 6271 -b 5971 -d 5
./generateGeom.py -t 5971 -b 5701 -d 5
./generateGeom.py -t 5701 -b 5371 -d 5
./generateGeom.py -t 5371 -b 3480 -d 0
./generateGeom.py -t 3480 -b 1221 -d 0
./generateGeom.py -t 1221 -b 0    -d 0
