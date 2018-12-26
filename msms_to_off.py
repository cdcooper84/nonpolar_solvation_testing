'''
This code transforms msms format meshes to .off, readable by trimesh
'''
import numpy
import os

problem_folder = 'mobley_test/'

for line in file('actually_all_names.txt'):

    mol = line[:-1]
    filename = problem_folder+mol+'/surf_d02'

    try: 
        vert = numpy.loadtxt(filename+'.vert')
        face = numpy.loadtxt(filename+'.face')

        f = open(filename+'.off','w')
        f.write('OFF\n%i %i 0\n\n'%(len(vert),len(face)))

        for i in range(len(vert)):
            f.write('%1.4f\t%1.4f\t%1.4f\n'%(vert[i,0],vert[i,1],vert[i,2]))

        for i in range(len(face)):
            f.write('3\t%i\t%i\t%i\n'%(face[i,0]-1,face[i,1]-1,face[i,2]-1))
        f.close()

    except:
        print mol
        print 'Could not generate off file'

