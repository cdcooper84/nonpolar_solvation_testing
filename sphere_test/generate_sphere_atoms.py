'''
This code generates xyzr and vdw files for an array of atoms
placed in a 0.5angs grid, that are inside a sphere. This follows
Bardhan, Jungwirth and Makowski, J. Chem. Phys. (2012).
'''
import numpy

c_vdw_rad = 1.9080
c_vdw_eps = 0.0860

stern_rad = 1.4

radius = 10.

h = 0.5

grid_points = numpy.arange(-radius, radius+h, h)
grid_x, grid_y, grid_z = numpy.meshgrid(grid_points, grid_points, grid_points)

N_side = len(grid_x)
N_total = N_side**3
grid_xyz = numpy.zeros((N_total,3))
for i in range(N_side):
    for j in range(N_side):
        for k in range(N_side):
            I = i*N_side*N_side + j*N_side + k
            grid_xyz[I,0] = grid_x[i,j,k]
            grid_xyz[I,1] = grid_y[i,j,k]
            grid_xyz[I,2] = grid_z[i,j,k]

grid_norm = numpy.sqrt(numpy.sum(grid_xyz**2, axis=1))

inside_atoms = numpy.where(grid_norm<(radius-c_vdw_rad-stern_rad))[0]

sphere_atoms = numpy.zeros((len(inside_atoms),4))
sphere_atoms[:,:3] = grid_xyz[inside_atoms, :]  
sphere_atoms[:,3]  = c_vdw_rad

numpy.savetxt('sphere_atoms.xyzr', sphere_atoms, fmt='%1.5f')

f = open('sphere_atoms.vdw','w')
for i in range(len(sphere_atoms)):
    f.write('C\t%1.5f\t%1.5f\n'%(c_vdw_rad, c_vdw_eps))

f.close()

