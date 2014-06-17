#! /usr/bin/python

import os

nThrough = []
failed = []
for file in os.listdir ('./output'):

  delete = False
  fileFields = file.split ('.')

  if file.endswith('.o'):
    f = open ('./output/' + file, 'r')

    for line in f:

      if line.startswith ('Radial region: '):
        fields = line.split (': ')
    
      if line.startswith ('N_through: '):
        fieldsThrough = line.split (': ')

      if line.startswith ('ERROR:'):
        failed.append (fields[1].rstrip())
        nThrough.append (fieldsThrough[1].rstrip())
        print 'Failed on: ' + failed[-1]
        delete = True
        break
  
    f.close () 
  
  if delete:
    os.remove ('./output/' + file)
    os.remove ('./output/' + fileFields[0] + '.' + fileFields[1] + '.e')

if failed:
  fo = open ('./drivers/refineDriver.sh', 'w')
  for reg, num in zip (failed, nThrough):
    fo.write ('sbatch ./submit/job_refineMesh.sbatch ' + reg + ' ' + num + '\n')
else:
  print 'No more failed jobs.'
