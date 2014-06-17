#! /usr/bin/python

f = open ('./drivers/geomDriver.sh', 'r')

radString = []
disString = []
for line in f:
  fields = line.split (' ')
  if fields[0] != 'sleep' and fields[0] != 'cd':

    radString.append ( 'rad' + fields[3] + '-' + fields[5] )

    if fields[7] == '0':
        fields[7] = 1

    disString.append ( str ( (int (fields[5]) - int (fields[3])) / int (fields[7])) )

f.close()

bad = ['rad3480-5371', 'rad1221-3480', 'rad0-1221']

f = open ('./drivers/refineDriver.sh', 'w')
for line, dis in zip (radString, disString):
  if line not in bad:
    f.write ('sbatch ./submit/job_refineMesh.sbatch ' + line + ' ' + dis + '\n')
f.close()
