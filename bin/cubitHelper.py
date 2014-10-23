import cubit
import os
from math import *

def deg2rad (deg):

    rad = deg * pi / 180.
    return rad

def colLatRad2xyz (col, lon, rad):

    x = rad * cos (lon) * sin (col)
    y = rad * sin (lon) * sin (col)
    z = rad * cos (col)

    return x, y, z

def lat2col (lat):

    col = 90 - lat
    return col

def surfLatLon2xyz (lat, lon):

    rad = 6371.
    col = lat2col (lat)
    
    x, y, z = colLatRad2xyz (deg2rad (col), deg2rad (lon), rad)
    return x, y, z 

R_EARTH = 6371.
radMin  = 3480.
name    = 'Kernel'
lat1, lon1 = input ('Enter lat/lon for corner 1: ')
lat2, lon2 = input ('Enter lat/lon for corner 2: ')
lat3, lon3 = input ('Enter lat/lon for corner 3: ')
lat4, lon4 = input ('Enter lat/lon for corner 4: ')

vcMinlMin = surfLatLon2xyz (lat1, lon1)
vcMaxlMin = surfLatLon2xyz (lat2, lon2)
vcMaxlMax = surfLatLon2xyz (lat3, lon3)
vcMinlMax = surfLatLon2xyz (lat4, lon4)
 
cubit.init ('.')
cubit.cmd  ('set journal off')

v0        = cubit.create_vertex (0, 0, 0)
zMax      = cubit.create_vertex (0, 0, vcMinlMin[2])
zMin      = cubit.create_vertex (0, 0, vcMaxlMax[2])
vcMinlMin = cubit.create_vertex (vcMinlMin[0], vcMinlMin[1], vcMinlMin[2])
vcMaxlMin = cubit.create_vertex (vcMaxlMin[0], vcMaxlMin[1], vcMaxlMin[2])
vcMaxlMax = cubit.create_vertex (vcMaxlMax[0], vcMaxlMax[1], vcMaxlMax[2])
vcMinlMax = cubit.create_vertex (vcMinlMax[0], vcMinlMax[1], vcMinlMax[2])
  
cubit.cmd ('create curve arc center vertex ' + str(v0.id())   + \
  ' ' + str(vcMinlMin.id()) + ' ' + str(vcMaxlMin.id()))      
cubit.cmd ('create curve arc center vertex ' + str(v0.id())   + \
  ' ' + str(vcMaxlMax.id()) + ' ' + str(vcMinlMax.id()))
cubit.cmd ('create curve arc center vertex ' + str(v0.id()) + \
  ' ' + str(vcMaxlMax.id()) + ' ' + str(vcMinlMin.id()))
cubit.cmd ('create curve arc center vertex ' + str(v0.id()) + \
  ' ' + str(vcMinlMax.id()) + ' ' + str(vcMaxlMin.id()))

cubit.cmd ( 'create sphere radius ' + str(R_EARTH) + \
  ' inner radius ' + str(radMin) ) 
cubit.cmd ( 'project curve 1 2 3 4 onto surface 1' ) 
cubit.cmd ( 'create surface curve 5 6 7 8 on surface 1' )
cubit.cmd ( 'thicken body 2 depth ' + str( R_EARTH - 1 ) + ' both' )
cubit.cmd ( 'intersect volume all' )
cubit.cmd ( 'delete vertex all' )
cubit.cmd ( 'delete curve all' )
cubit.cmd ( 'compress' )
cubit.cmd ( 'vol 1 name "' + name + '_cutter"' )

cubit.cmd ('save as "./kernel_cutter.cub" overwrite' )
