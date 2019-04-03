import numpy
#import xml.etree.ElementTree as ET
from argparse import ArgumentParser

parser = ArgumentParser(description='Inputs')
parser.add_argument('-gaff', '--gaff_file', dest='gaff_file', type=str, default=None, help='Path to gaff.dat file with parameters')
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

