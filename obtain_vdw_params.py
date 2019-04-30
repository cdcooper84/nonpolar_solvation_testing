import numpy
#import xml.etree.ElementTree as ET
from argparse import ArgumentParser

parser = ArgumentParser(description='Inputs')
parser.add_argument('-gaff', '--gaff_file', dest='gaff_file', type=str, default=None, help='Path to gaff.dat file with parameters. Here use: /usr/share/openbabel/2.3.2/gaff.dat')
parser.add_argument('-prmtop', '--prmtop_file', dest='prmtop_file', type=str, default=None, help='Path to prmtop file (from Mobley09 supp info)')
parser.add_argument('-pqr', '--pqr_file', dest='pqr_file', type=str, default=None, help='Path to pqr file')
parser.add_argument('-vdw', '--vdw_file', dest='vdw_file', type=str, default=None, help='File name of output')

args = parser.parse_args()


#tree = ET.parse(xml_file)
#root = tree.getroor()

gaff_data = []
flag = False
for line in file(args.gaff_file):
    line = line.split()

    if len(line)>0 and line[0] == 'MOD4':
        flag = True

    if flag and len(line)>2:
        gaff_data.append([line[0], line[1], line[2]])
        
    if len(line)>0 and flag and line[0] == 'END':
        flag = False

flag = 0
for line in file(args.prmtop_file):

    line = line.split()

    if len(line)>0:
        if line[-1] == 'AMBER_ATOM_TYPE':
            flag += 1
        elif flag == 1:
            flag += 1
        elif flag == 2:
            atom_type = line
            flag = 0

outfile = open(args.vdw_file, "w")
i = 0
for line in file(args.pqr_file):
    line = line.split()

    atom_name = line[2]
    atom_radius = line[-1]

    # should do this with a dictionary
    atom_eps = 'None'
    for j in range(len(gaff_data)): 
        if atom_type[i] == gaff_data[j][0]:
            atom_eps = gaff_data[j][2]

    if atom_eps=='None':
        print('Couldnt find atom_eps for '+atom_name)
    else:
        outfile.write(atom_name+'\t'+atom_type[i]+'\t'+atom_radius+'\t'+atom_eps+'\n')

    i += 1

outfile.close()

'''
outfile = open(args.vdw_file, "w")
for line in file(args.pqr_file):
    line = line.split()

    atom_name = line[2]
    atom_radius = line[-1]

    found = False
    for i in range(len(gaff_data)):
        if gaff_data[i][0] == atom_name.lower() and abs(float(atom_radius)-float(gaff_data[i][1]))<1e-8:
            atom_eps = gaff_data[i][2]
            
            found = True
            outfile.write(atom_name+'\t'+atom_radius+'\t'+atom_eps+'\n')
            break

    if found == False:
        print 'Coudnt find atom with exact name for '+atom_name+', first closest name'
        for i in range(len(gaff_data)):
            if gaff_data[i][0] in atom_name.lower() and abs(float(atom_radius)-float(gaff_data[i][1]))<1e-8:
                atom_eps = gaff_data[i][2]
                
                found = True
                outfile.write(atom_name+'\t'+atom_radius+'\t'+atom_eps+'\n')
                break

    if found == False:
        print 'Coudnt find atom with name for '+atom_name+', trying radii'
        for i in range(len(gaff_data)):
            if abs(float(atom_radius)-float(gaff_data[i][1]))<1e-8:
                atom_eps = gaff_data[i][2]
            
                print 'Found for '+gaff_data[i][0]
                
                found = True
                outfile.write(atom_name+'\t'+atom_radius+'\t'+atom_eps+'\n')
                break

    if found == False:
        print 'Coudnt find atom with radii for '+atom_name

outfile.close()
'''

