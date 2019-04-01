'''
This script copies xyzr from Jay (which are scaled by 0.9),
scales back, and saves a new xyzr. Then, it generates a xyzr
for Stern layer and then generates the mesh
'''
import os
import numpy

problem_folder = '/Users/chris/Dropbox/lab/Projects/slic-jctc-mnsol/nlbc-mobley/nlbc_test/'

for line in file('actually_all_names.txt'):

    mol = line[:-1]

    # Generate folder for molecule
    cmd = 'mkdir ' + mol 
    os.system(cmd)

    # Get xyzr from Jay (and rescale by 1/0.9)
    print problem_folder + mol + '/test.xyzr' 
    xyzr = numpy.loadtxt(problem_folder + mol + '/test.xyzr')
    xyzr[:,3] *= 1/0.92
    numpy.savetxt(mol+'/radii.xyzr', xyzr, fmt='%1.3f')

    # Create xyzr for Stern layer
    xyzr[:,3] += 1.4
    numpy.savetxt(mol+'/radii_stern.xyzr', xyzr, fmt='%1.3f')

    # Generate mesh of dielectric interface
    cmd = 'msms -if ' + mol + '/radii.xyzr -of ' + mol + '/surf_d02 -d 2 -p 1.4 -no_header'
    os.system(cmd)

    # Generate mesh of Stern layer 
    cmd = 'msms -if ' + mol + '/radii_stern.xyzr -of ' + mol + '/surf_d02_stern -d 2 -p 0.01 -no_header'
    os.system(cmd)
