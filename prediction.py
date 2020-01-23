
import sys
from parsers import TsvReader
import os
from Model import Model

def str2float(x):

    try:
        return float(x)
    except:
        return None

def main():

    if len(sys.argv) < 4:
        print >> sys.stderr, 'python xxx.py <ind list> <pheno file> <ind dir>'
        sys.exit()

    indfile = sys.argv[1]
    phenofile = sys.argv[2]
    inddir = sys.argv[3]

    indlist = [x.rstrip() for x in open(indfile,'r').readlines()]
    phenolist = [x.rstrip().split('\t')[1] for x in \
        open(phenofile,'r').readlines()]

    for ind in indlist:
        if not os.path.exists(inddir+'/'+ind):
            print >> sys.stderr, 'Individual directory does not exist:',\
                inddir+'/'+ind
            continue

        fh = open(inddir+'/'+ind+'/unknown-penetrance.txt','r')
        pheno2unk = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/lvs-penetrance.txt','r')
        pheno2lvs_pen = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/lgs-penetrance.txt','r')
        pheno2lgs_pen = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/hgs-penetrance.txt','r')
        pheno2hgs_pen = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/hvs.txt','r')
        pheno2hvs_pen = dict(map(lambda x: (x[0],str2float(x[2])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/lvs.txt','r')
        pheno2lvs = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/lgs.txt','r')
        pheno2lgs = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/hgs.txt','r')
        pheno2hgs = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))
        fh = open(inddir+'/'+ind+'/hvs.txt','r')
        pheno2hvs = dict(map(lambda x: (x[0],str2float(x[1])), \
            [y.rstrip().split('\t') for y in fh.readlines()]))

        out = open(inddir+'/'+ind+'/prediction.txt','w')
        for pheno in phenolist:

            lvs_pen = 0.0
            lgs_pen = 0.0
            hgs_pen = 0.0
            hvs_pen = 0.0
            lvs = 0.0
            lgs = 0.0
            hgs = 0.0
            hvs = 0.0

            if not pheno in pheno2unk or pheno2unk[pheno] == None:
                out.write(pheno+'\tNA\n')
                continue

            if pheno in pheno2lvs_pen and pheno2lvs_pen[pheno] != None:
                lvs_pen = pheno2lvs_pen[pheno]
            if pheno in pheno2lgs_pen and pheno2lgs_pen[pheno] != None:
                lgs_pen = pheno2lgs_pen[pheno]
            if pheno in pheno2hgs_pen and pheno2hgs_pen[pheno] != None:
                hgs_pen = pheno2hgs_pen[pheno]
            if pheno in pheno2hvs_pen and pheno2hvs_pen[pheno] != None:
                hvs_pen = pheno2hvs_pen[pheno]
            if pheno in pheno2lvs and pheno2lvs[pheno] != None:
                lvs = pheno2lvs[pheno]
            if pheno in pheno2lgs and pheno2lgs[pheno] != None:
                lgs = pheno2lgs[pheno]
            if pheno in pheno2hgs and pheno2hgs[pheno] != None:
                hgs = pheno2hgs[pheno]
            if pheno in pheno2hvs and pheno2hvs[pheno] != None:
                hvs = pheno2hvs[pheno]

            model = Model()
            model.setValues(lvs,lgs,hgs,hvs,pheno2unk[pheno], \
                lvs_pen,lgs_pen,hgs_pen,hvs_pen)
            prediction = model.runModel()
            out.write(pheno+'\t'+str(prediction)+'\n')
        out.close()

if __name__ == '__main__': main()

