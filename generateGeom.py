#! /usr/bin/python2.6

import cubit
import sys
import os

fNameBase = 'save as "/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/masters/'

if ( len (sys.argv) < 2 or sys.argv[1] == '-h' ):
  sys.exit ( 'Usage: ./generateGeom -t <val> -b <val> -d <val> \
    \n-t: top layer (radius, [m]) \n-b: bottom layer (radius [m]) \
    \n-d: radial discretization [m]' )

for i in range (len (sys.argv) - 1 ):
  if sys.argv[i] == '-t':
    top = int (sys.argv[i+1])
  if sys.argv[i] == '-b':
    bot = int (sys.argv[i+1])
  if sys.argv[i] == '-d':
    dis = int (sys.argv[i+1])
    
fSub  = '.rad' + str(bot).zfill(4) + '-' + str(top).zfill(4) + \
  '.000.cub" overwrite journal'

if ( bot >= top ):
  sys.exit ('Bottom is greater than top. Try again.')

cubit.init ('.')
cubit.cmd  ('set journal off')

if ( bot != 0 ):
  cubit.cmd  ( 'create sphere radius %d inner radius %d ' % (top, bot) +
    'xpositive ypositive zpositive' )
else:
  cubit.cmd ( 'create sphere radius ' + str (top) + ' xpos ypos zpos')
  
cubit.cmd ( 'vol 1 name "masters"' )

if ( dis != 0 ):
  for i, rad in enumerate (range (top-dis, bot+dis, dis * (-1))):
    cubit.cmd ( 'create sphere radius ' + str (rad) )
    cubit.cmd ( 'webcut vol ' + str (i+1) + ' with tool vol ' + str (i+2) )
    cubit.cmd ( 'delete vol ' + str (i+2) )
    cubit.cmd ( 'compress all' )
    
  cubit.cmd ( 'imprint volume all\n' )
  cubit.cmd ( 'merge volume all\n' )
      
cubit.cmd ( "group 'Masters' equals Volume all\n" )

cubit.cmd ( fNameBase + 'col000-090.lon000-090' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( fNameBase + 'col000-090.lon090-180' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( fNameBase + 'col000-090.lon180-270' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( fNameBase + 'col000-090.lon270-360' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( 'volume all reflect Z\n' )
cubit.cmd ( fNameBase + 'col090-180.lon000-090' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( fNameBase + 'col090-180.lon090-180' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( fNameBase + 'col090-180.lon180-270' + fSub + '\n' )
cubit.cmd ( 'rotate volume all angle 90 about z include_merged\n' )
cubit.cmd ( fNameBase + 'col090-180.lon270-360' + fSub + '\n' )

if ( cubit.get_error_count() != 0 ):
  print "I'm sorry to say that I've detected some errors."

cubit.cmd ( 'quit' )