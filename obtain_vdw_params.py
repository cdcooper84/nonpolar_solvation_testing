import numpy
#import xml.etree.ElementTree as ET
from argparse import ArgumentParser

parser = ArgumentParser(description='Inputs')
parser.add_argument('-gaff', '--gaff_file', dest='gaff_file', type=str, default=None, help='Path to gaff.dat file with parameters. Here use: /usr/share/openbabel/2.3.2/gaff.dat')
parser.add_argument('-prmtop', '--prmtop_file', dest='prmtop_file', type=str, default=None, help='Path to prmtop file (single) or folder (with list_file) (from Mobley09 supp info)')
parser.add_argument('-pqr', '--pqr_file', dest='pqr_file', type=str, default=None, help='Path to pqr file (only single)')
parser.add_argument('-vdw', '--vdw_file', dest='vdw_file', type=str, default=None, help='File name of output (only single)')
parser.add_argument('-list','--list_file', dest='list_file', type=str, default=None, help='File with list of molecule names')
parser.add_argument('-folder','--folder_list', dest='folder_list', type=str, default=None, help='Folder where molecules from list_file are (only with list file)')

args = parser.parse_args()

def generate_vdw_file(args, gaff_data):
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
                flag += 1
            elif flag == 3:
                if line[0]!='%FLAG':
                    atom_type.extend(line)
                    flag = 0
                else:
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

if args.list_file==None:
    generate_vdw_file(args, gaff_data)
else:
    prmtop_folder = args.prmtop_file
    for line in file(args.list_file):
        if line[-1:]=='\n':
            mol_name = line[:-1]
        else:
            mol_name = line
        print mol_name
        args.pqr_file = args.folder_list+mol_name+'/'+mol_name+'.pqr'
        args.vdw_file = args.folder_list+mol_name+'/'+mol_name+'.vdw'
        args.prmtop_file = prmtop_folder+mol_name+'.prmtop'
        generate_vdw_file(args, gaff_data)
