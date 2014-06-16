#! /usr/bin/python2.6

import os
import sys
import cubit

from math import sin, cos, pi

def colLonRad2xyz (col, lon, rad):
  
  col = col * pi / 180.
  lon = lon * pi / 180.
  
  x = rad * sin(col) * cos(lon)
  y = rad * sin(col) * sin(lon)
  z = rad * cos(col)
  
  return (x, y, z)

R_EARTH  = 6371.
geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom'

name   = str ( raw_input ('Enter region name: '))
colMax = input ('Enter max collatitude: ')
colMin = input ('Enter min collatitude: ')
lonMax = input ('Enter max longitude: ')
lonMin = input ('Enter min longitude: ')
radMax = input ('Enter max radius: ')
radMin = input ('Enter min radius: ')
rotAng = input ('Enter rotation angle [degrees]: ')

if rotAng != 0:
  rotX   = input ('Enter X vector: ')
  rotY   = input ('Enter Y vector: ')
  rotZ   = input ('Enter Z vector: ')

if radMin >= radMax or lonMin >= lonMax or colMin >= colMax :
  raise ValueError ('Min is greater than max in one of your specifications.') 

if ( lonMax > 180. ):
  lonMax = lonMax - 360.

vcMinlMin = colLonRad2xyz ( colMin, lonMin, R_EARTH )
vcMaxlMin = colLonRad2xyz ( colMax, lonMin, R_EARTH )
vcMaxlMax = colLonRad2xyz ( colMax, lonMax, R_EARTH )
vcMinlMax = colLonRad2xyz ( colMin, lonMax, R_EARTH )
 
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
cubit.cmd ('create curve arc center vertex ' + str(zMin.id()) + \
  ' ' + str(vcMaxlMax.id()) + ' ' + str(vcMaxlMin.id()))
cubit.cmd ('create curve arc center vertex ' + str(zMax.id()) + \
  ' ' + str(vcMinlMax.id()) + ' ' + str(vcMinlMin.id()))

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

if rotAng != 0.:
  cubit.cmd('rotate volume 1 angle ' + str(-1 * rotAng) + \
    ' about origin 0 0 0 direction ' + str(rotX) + ' ' + \
    str(rotY) + ' ' + str(rotZ) + ' include_merged')
    
cubit.cmd ('save as "' + geomPath + '/cutters/' + name + \
  '_cutter.cub" overwrite' )