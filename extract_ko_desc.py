#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
from collections import defaultdict

__author__ = "Florian Plaza Oñate"
__email__ = "fplaza-onate@enterome.com"

def is_file(path):
    """Check if path is an existing file.
    """

    if not os.path.isfile(path):
        if os.path.isdir(path):
            msg = "{0} is a directory".format(path)
        else:
            msg = "{0} does not exist.".format(path)
            raise argparse.ArgumentTypeError(msg)
    return path

def get_parameters():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--ko-pathway', dest='ko_pathway_list', required=True, type=is_file,
            help='')

    parser.add_argument('--pathway', dest='pathway_list', required=True, type=is_file,
            help='')

    parser.add_argument('--ko-desc', dest='ko_desc', required=True,
            help='')

    return parser.parse_args()

def get_ko_pathways(ko_pathway_list):
    ko_pathways=defaultdict(set)
    with open(ko_pathway_list, 'r') as ifs:
        for line in ifs:
            ko_name,pathway_name =line.split()
            ko_name=ko_name[3:]

            if pathway_name.startswith('path:map'):
                pathway_name = pathway_name[8:]
            elif pathway_name.startswith('path:ko'):
                pathway_name=pathway_name[7:]

            ko_pathways[ko_name].add(pathway_name)
    return ko_pathways

def get_pathway_desc(pathway_list):
    pathway_desc=dict()
    with open('pathway.list', 'r') as pathway_list:
        for line in pathway_list:
            line=line.rstrip()
            if line.startswith('##'):
                pathway_subcategory=line[2:]
            elif line.startswith('#'):
                pathway_category=line[1:]
            else:
                pathway_name,pathway_txt=line.split('\t')
                pathway_desc[pathway_name]=(pathway_category, pathway_subcategory, pathway_txt)

    return pathway_desc

def print_ko_desc(ko_pathways, pathway_desc, ko_desc):
    with open(ko_desc, 'w') as ofs:
        for ko_name in sorted(ko_pathways.keys()):
            for pathway_name in ko_pathways[ko_name]:
                pathway_category, pathway_subcategory, pathway_txt = pathway_desc[pathway_name]
                print('\t'.join([ko_name, pathway_name, pathway_category, pathway_subcategory, pathway_txt]), file=ofs)

def main():
    parameters = get_parameters()
    ko_pathways=get_ko_pathways(parameters.ko_pathway_list)
    pathway_desc=get_pathway_desc(parameters.pathway_list)
    print_ko_desc(ko_pathways, pathway_desc, parameters.ko_desc)

if __name__ == '__main__':
    main()

