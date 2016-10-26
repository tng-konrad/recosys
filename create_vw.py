# -*- coding: utf-8 -*-

# this script demonstrates how to convert a tabulated file (csv, but easy to adapt to other separators)
# into Vowpal Wabbit format
# the key idea is to define groups of columns (manually) corresponding to namespaces 
# data used here as a basis comes from the Outbrain contest on Kaggle
# https://www.kaggle.com/c/outbrain-click-prediction

import os
import subprocess
from collections import defaultdict, Counter
from datetime import datetime, date
from csv import DictReader
import math
from glob import glob
import copy
from numpy import loadtxt


if __name__ == '__main__':

    # define groups of columns
    
    fname = 'xtest_v1'
    totcount = 0
    num_cols = ['doccnt','geocnt','uidcnt', 
                'platcnt','campcnt','advcnt' , 'tst']    
    cat_cols = ['adid','docid', 'uuid', 'plat', 'geoloc', 'docid2' ]                   
    # 'dispid'
 
    with open('../input/'+fname+'.vw',"wb") as outfile:
        for linenr, row in enumerate( DictReader(open('../input/'+fname+'.csv',"rb")) ):
            
            # declare the contents of workspaces
            n_c = ''; n_n = ''
            label = -1
            ID = row['dispid'] + 'x' + row['adid']
            if linenr % 1000000 == 0:
                print('Read {} lines...'.format(linenr))
                # print(str(totcount) ) 
            # print(row.keys())
            for kk in row.keys():
                if kk == 'clicked':                
                    label = 2 * int(row[kk]) - 1
                else:
                    if kk in cat_cols: 
                        if row[kk] != '':
                            n_c += " %s_%s"%(kk,row[kk])
                    elif kk in num_cols: 
                            n_n += " %s:%s"%(kk,str(float(row[kk])))
            outfile.write("%s '%s |c%s|n%s \n"%(label,ID, n_c, n_n))
            totcount += (label + 1)/2.0
            
