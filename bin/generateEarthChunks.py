#! /usr/bin/python2.6

import cubit
import time
import sys
import os

if ( len (sys.argv) < 2 or sys.argv[1] == '-h' ):
  sys.exit ( 'Usage: ./generateGeom -t <val> -b <val> -d <val> \
    \n-t: top layer (radius, [m]) \n-b: bottom layer (radius [m]) \
    \n-d: radial discretization [m] \
    \n-f: write directory' )

for i in range (len (sys.argv) - 1 ):
  if sys.argv[i] == '-t':
    top = int (sys.argv[i+1])
  if sys.argv[i] == '-b':
    bot = int (sys.argv[i+1])
  if sys.argv[i] == '-d':
    dis = int (sys.argv[i+1]) * -1
  if sys.argv[i] == '-f':
    saveDir = (sys.argv[i+1])
    
fNameBase = 'save as "' + saveDir


if ( bot >= top ):
    sys.exit ('Bottom is greater than top')

time.sleep(1)

cubit.init ('.')
cubit.cmd  ('set journal off')

for rad in range (top, bot, dis):
  
  cubit.cmd ('create sphere radius %d inner radius %d ' % (rad, rad-abs(dis)) + 
    'xpositive ypositive zpositive' )

  fSub  = '.rad' + str(rad-abs(dis)).zfill(4) + '-' + str(rad).zfill(4) + \
    '.000.cub" overwrite journal'

  cubit.cmd ( 'vol 1 name "masters"' )
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

  cubit.cmd ( 'reset' )

if ( cubit.get_error_count () != 0 ):
  print "I'm so sorry, but I've detected errors. Check."

cubit.cmd ( 'quit' )
