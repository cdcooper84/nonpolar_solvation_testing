import numpy
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

parser = ArgumentParser(description='Inputs')
parser.add_argument('-xml', '--xml_file', dest='xml_file', type=str, default=None, help='Path to xml file with parameters')
parser.add_argument('-pqr', '--pqr_file', dest='pqr_file', type=str, default=None, help='Path to pqr file')

tree = ET.parse(xml_file)
root = tree.getroor()

for line in pqr_file:
    line = line.split()

    atom_name = line[2]
    atom_radius = line[-1]

    for i in range(len(root)):
        root[i][1][3].text
