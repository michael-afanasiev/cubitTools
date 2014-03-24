#! /usr/local/bin/python

import subprocess
import os

top = int ( raw_input ('Top layer [radius]\n') )
bot = int ( raw_input ('Bottom layer [radius]\n') )
dis = int ( raw_input ('Radial discretization\n') ) * (-1)
opt = int ( raw_input ('[0] Layers \n[1] Center\n'))

if opt == 0:
  optString = 'surface'
if opt == 1:
  optString = 'volume'

domains = []
domains.append('xpositive ypositive zpositive')

fNameBase = 'save as "/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/masters/'
tPath     = "/Applications/Trelis-15.0.app/Contents/MacOS/Trelis-15.0"

for domain in domains:
  
  if domain == domains[0]:
    fName = 'col0-90.lon0-90'
    
  fSub  = '.rad' + str(bot).zfill(4) + '-' + str(top).zfill(4) + \
    '.000.cub" overwrite journal'
  fPath = "./template" + str(top) + ".jou"
  
  file = open (fPath, 'w')

  tSurf      = 1
  bSurf      = 5
  surfString = ''
  i = 1
  for rad in range (top, bot, dis):
  
    if opt == 0:
      file.write ('create sphere radius %d inner radius %d ' % 
      (rad, rad-abs(dis)) + domain + "\n" )
      file.write ('vol ' + str(i) + ' name "masters' + str(i) + '"\n')
      i = i + 1
    
    if opt == 1:
      file.write ('create sphere radius %d' % (rad) + domain + "\n" )
      file.write ('vol 1 name masters \n')
        
    surfString = surfString + ' ' + str (tSurf) + ' ' + str (bSurf)
    bSurf = bSurf + 5
    tSurf = tSurf + 5
    
  file.write ( "group 'Surfs' equals Surface " + surfString + '\n' )
  file.write ( "group 'Masters' equals Volume all\n" )
  
  if opt == 0:
    file.write ( 'imprint volume all\n' )
    file.write ( 'merge volume all\n' )

  file.write ( fNameBase + 'col000-090.lon000-090' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  file.write ( fNameBase + 'col000-090.lon090-180' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  file.write ( fNameBase + 'col000-090.lon180-270' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  file.write ( fNameBase + 'col000-090.lon270-360' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  
  file.write ( 'volume all reflect Z\n' )
  
  file.write ( fNameBase + 'col090-180.lon000-090' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  file.write ( fNameBase + 'col090-180.lon090-180' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  file.write ( fNameBase + 'col090-180.lon180-270' + fSub + '\n' )
  file.write ( 'rotate volume all angle 90 about z include_merged\n' )
  file.write ( fNameBase + 'col090-180.lon270-360' + fSub + '\n' )
  
  file.write ( 'quit' )
  file.close ( )
      
  subprocess.call ([tPath + " -nographics " + fPath], shell=True, stdout=None)