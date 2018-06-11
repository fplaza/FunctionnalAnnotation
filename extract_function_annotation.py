#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract a set of sequences from a Multi-FASTA file"""

from __future__ import print_function
import argparse
import os
from collections import OrderedDict, defaultdict

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2015, Enterome"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Florian Plaza Oñate"
__email__ = "fplaza-onate@enterome.com"
__status__ = "Development"

class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory

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
    """Parse command line parameters.
    """
    parser = argparse.ArgumentParser(description=__doc__)


    parser.add_argument('-i', '--hits', dest='hits_file', type=is_file, required=True,
            help='Query genes vs KEGG genes hits (blastp or diamond, tabular output format)')

    parser.add_argument('-k', '--ko-genes', dest='ko_genes_file', type=is_file, required=True,
            help='File which associate each KEGG gene to a KO')

    parser.add_argument('-o', '--functionnal-annotation', dest='functionnal_annotation_file', required=True,
            help='Output file which contains functionnal annotation of query genes')

    return parser.parse_args()

def index_kegg_genes(ko_genes_file):
    kegg_gene_to_ko = dict()
    with open(ko_genes_file, 'r') as istream:
        for line in istream:
            ko, gene = line.rstrip().split('\t')	
            kegg_gene_to_ko[gene]=ko[3:]
    return kegg_gene_to_ko

def extract_functionnal_annotation(kegg_gene_to_ko, hits_file):
    query_genes_all_kos=OrderedDefaultDict(OrderedDict)
    with open(hits_file, 'r') as istream:
        for line in istream:
            line_items = line.split()
            query_gene, kegg_gene = line_items[:2]
            bitscore = line_items[11]
            ko = kegg_gene_to_ko[kegg_gene]

            if (query_gene not in query_genes_all_kos) or (ko not in query_genes_all_kos[query_gene]):
                query_genes_all_kos[query_gene][ko] = bitscore

    return query_genes_all_kos

def write_functionnal_annotation(query_genes_all_kos, functionnal_annotation_file):
    with open(functionnal_annotation_file,'w') as ostream:
        print('gene_name\tko\tbitscore', file=ostream)
        for query_gene, all_kos in query_genes_all_kos.iteritems():
            for ko, bitscore in all_kos.iteritems():
                print('{0}\t{1}\t{2}'.format(query_gene, ko, bitscore), file=ostream)

def main():
    parameters = get_parameters()

    print('Indexing KEGG genes...')
    kegg_gene_to_ko=index_kegg_genes(parameters.ko_genes_file)
    print('Done. {0} KEGG genes indexed.\n'.format(len(kegg_gene_to_ko)))

    print('Extracting query genes functionnal annotation...')
    query_genes_all_kos=extract_functionnal_annotation(kegg_gene_to_ko, parameters.hits_file)
    print('Done. {0} query genes annotated.\n'.format(len(query_genes_all_kos)))

    print('Write query genes functionnal annotation...')
    write_functionnal_annotation(query_genes_all_kos, parameters.functionnal_annotation_file)
    print('Done.\n')


if __name__ == '__main__':
    main()

