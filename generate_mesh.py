'''
This script copies xyzr from Jay (which are scaled by 0.92),
scales back, and saves a new xyzr. Then, it generates a xyzr
for Stern layer and then generates the mesh
'''
import os
import numpy

problem_folder = '/home/chris/Dropbox/lab/Projects/slic-jctc-mnsol/nlbc-mobley/nlbc_test/'

for line in file('actually_all_names.txt'):

    mol = line[:-1]

    # Generate folder for molecule
    cmd = 'mkdir ' + 'mobley_test/' +  mol 
    os.system(cmd)

    # Get xyzr from Jay (and rescale by 1/0.92)
    filename_in = problem_folder + mol + '/test.pqr'
    print filename_in

    filename_pqr = 'mobley_test/' + mol + '/' + mol + '.pqr'
    filename_xyzr = 'mobley_test/'  + mol + '/' + mol + '.xyzr'
    filename_xyzr_stern = 'mobley_test/'  + mol + '/' + mol + '_stern.xyzr'
    
    file_pqr = open(filename_pqr, "w")
    file_xyzr = open(filename_xyzr, "w")
    file_xyzr_stern = open(filename_xyzr_stern, "w")

    for line in file(filename_in):
        line_split = line.split()

        if len(line_split)>0:
            if line_split[0] == 'ATOM':
                if len(line_split[5:-2])==3:
                    x,y,z = [i for i in line_split[5:-2]]
                else:
                    x = line_split[5]
                    if '-' in x[1:]:
                        split_loc = line_split[5].find('-')
                        x = line_split[5][:split_loc]
                        y = line_split[5][split_loc:]
                        if '-' in y[1:]:
                            split_loc = y[1:].find('-')
                            z = y[split_loc:]
                            y = y[:split_loc]
                        else:
                            z = line_split[6]

                    else:
                        y = line_split[6]
                        if '-' in y[1:]:
                            split_loc = line_split[6].find('-')
                            y = line_split[6][:split_loc]
                            z = line_split[6][split_loc:]

                q = line_split[-2]
                r = line_split[-1]
                
                new_r = '%1.6f'%(float(r)/0.92)
                stern_r = '%1.6f'%(float(r)/0.92+1.4)

                line_prev = line_split[0]+'\t'+line_split[1]+'\t'+line_split[2]+'\t'+line_split[3]+'\t'+line_split[4]

                file_pqr.write(line_prev+'\t'+x+'\t'+y+'\t'+z+'\t'+q+'\t'+new_r+'\n')
                file_xyzr.write(x+'\t'+y+'\t'+z+'\t'+new_r+'\n')
                file_xyzr_stern.write(x+'\t'+y+'\t'+z+'\t'+stern_r+'\n')

    file_pqr.close()
    file_xyzr.close()
    file_xyzr_stern.close()

    # Generate mesh of dielectric interface
    cmd = 'msms -if '+filename_xyzr+' -of mobley_test/' + mol + '/surf_d02 -d 2 -p 1.4 -no_header'
    os.system(cmd)

    # Generate mesh of Stern layer 
    cmd = 'msms -if '+filename_xyzr_stern+' -of mobley_test/' + mol + '/surf_d02_stern -d 2 -p 0.01 -no_header'
    os.system(cmd)
