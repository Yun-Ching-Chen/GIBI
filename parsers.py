#! /usr/bin/env python

import sys, os
import re
import bz2

from optparse import OptionParser

def get_number(s):
    try:
        float(s)
        return float(s)
    except ValueError:
        return 'NA'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CmdOpts(object):
    usage="""%prog [options] -f 


    """

    def __init__(self):
        parser = OptionParser(usage=CmdOpts.usage)
        parser.add_option("-f", "--fname", dest="filename",
                          help="""Input gff file""")
        (opts, args) = parser.parse_args()

        if not opts.filename:
            parser.error("Incorrect input args")
            
        self.__dict__.update(opts.__dict__)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TsvReader(object):

    def __init__(self, filename,delim):
        self.fh = None
        if filename.endswith('bz2'):
            self.fh = bz2.BZ2File(filename,'r')
        else:
            self.fh = file(filename,'r')
        self.delim = delim
	#h1 = self.fh.readline()        # skip line 1

    def __iter__(self):
        return self

    def next(self):
        while True:
            line = self.fh.readline()
            if line == "":
                self.fh.close()
                raise StopIteration
            if line.startswith("#"):
                continue
            if line == "\n":
                continue
            return re.split(self.delim, line[:-1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DirReader(object):

    def __init__(self,dirname,substring,flags = 0):
        self.filelist = os.listdir(dirname)
        self.substring = substring
        self.path = dirname
        self.i = 0
        self.flags = flags

    def __iter__(self):
        return self

    def next(self):
        while True:
            if self.i == len(self.filelist):
                raise StopIteration
            if self.substring == "":
                self.i += 1
                return self.filelist[self.i-1]
            else:
                if re.search(self.substring,self.filelist[self.i],self.flags) != None:
                    self.i += 1
                    return self.filelist[self.i-1]
                else:
                    self.i += 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Config(object):

    def __init__(self,fname):
        self.argdict = {}
        for x in TsvReader(fname," *= *"):
            self.argdict[x[0]] = x[1]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Variant(object):

    def __init__(self, row):
        self.sampledb = row[0]
        self.uid = row[1]
        self.indexstring = row[2]
        self.coverage = row[3]
        self.mutcount = row[4]
        self.acount = row[5]
        self.ccount = row[6]
        self.gcount = row[7]
        self.tcount = row[8]
        self.sumqualityscore = row[9]
        self.minqualityscore = row[10]
        self.maxqualityscore = row[11]
        self.averagequalityscore = row[12]
        self.forward = row[13]
        self.reverse = row[14]
        self.distinctcoverage = row[15]
        self.distincttags = row[16]
        self.distinctpair = row[17]
        self.muttype = row[18]
        self.chrom = row[19]
        self.start = row[20]
        self.end = row[21]
        self.basefrom = row[22]
        self.baseto = row[23]
        self.transcript = row[24]
        self.txchangestart = row[25]
        self.txchangeend = row[26]
        self.txbasefrom = row[27]
        self.txbaseto = row[28]
        self.aminostart = row[29]
        self.aminoend = row[30]
        self.aafrom = row[31]
        self.aato = row[32]
        self.snp = row[33]
        self.deleted = row[34]
        self.comment = row[35]

    def __repr__(self):
    	return "\t".join([self.chrom])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    
    opts = CmdOpts()
    count=1
    for variant in TsvReader(opts.filename):
        if variant.basefrom == variant.txbasefrom:
            strand = '+'
        else:
            strand = '-'

            # print out the change in genomic format                                                                                 
        sys.stdout.write('\t'.join([str(count), variant.chrom,\
                                    str(int(variant.start)-1),\
                                    variant.end,\
                                    strand,\
                                    variant.txbasefrom,
                                    variant.txbaseto,variant.sampledb.replace(' ','')]) + '\n')
        count=count+1


if __name__ == "__main__":
   main()
