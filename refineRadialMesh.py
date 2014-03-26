#! /usr/bin/python2.6

import os
import sys
import cubit

path     = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/'
geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/'
  
cubit.init ('.')

for file in os.listdir ( geomPath + 'regions_meshed/' ):
  
  fields      = file.split ('.')
  radRegion   = fields[2]
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2'
    
  cubit.cmd  ('open "' + geomPath + 'regions_meshed/' + file + '"')
  cubit.cmd  ('compress all')
      
  if ( radRegion == 'rad5371-5701' or radRegion == 'rad5701-5971' or 
       radRegion == 'rad5971-6271' or radRegion == 'rad6271-6319' or 
       radRegion == 'rad6319-6351' or radRegion == 'rad6351-6371' ):
       
    surfs = [i for i in range (1, cubit.get_surface_count()+1)]
       
    targets = []
    for surf in surfs:
      if ( cubit.get_surface_type (surf) == 'sphere surface' ):
        targets.append (str ( surf ))
    
    refineString = 'Refine min_through_thickness 10 source surface ' + \
      targets[0] + ' target surface ' + targets[1] + ' anisotropic'
      
    cubit.cmd ( refineString )
    cubit.cmd ( 'export mesh "' + path + 'mesh/refined/' + exoFileName + 
      '" overwrite' )
    sys.exit()