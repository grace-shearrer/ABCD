# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:09:15 2018
script to get ABCD data going
@author: nibl
"""
import subprocess
import glob
import os
import pdb
import fnmatch

def cor_maker(basedir, workdir):
    biglist=glob.glob(os.path.join(basedir,'*.tgz'))
    for item in biglist:
        x=item.split('/')[4].split('_')[0]
        print(x)
        #check for the folder 
        folder = 'sub-%s'%(x)
        output = os.path.join(workdir, folder, 'derivative')
        
        if os.path.exists(os.path.join(workdir,folder)):
            print('FOLDER EXISTS')
            if os.path.exists(output) == False:
                os.makedirs(output)
                
            inputpath = glob.glob(os.path.join(workdir,folder,'ses-baselineYear1Arm1','func','*.nii'))
            for img in inputpath:
                restcall = 'python /Users/nibl/Desktop/ABCD/scripts/rsfmri_python/bin/resting_pipeline.py --func %s --steps 3,7  --outpath %s'%(img,output)
                print(restcall)
                runrest = subprocess.Popen(restcall, shell = True)
                runrest.wait()
                pdb.set_trace()
            continue
        else:
            matching = [s for s in biglist if x in s]
            print(matching)
            for item in matching:
                zippi = 'tar -xzvf %s -C %s'%(item,workdir)
                print(zippi)
                call=subprocess.Popen(zippi, shell = True)
                call.wait()
        pdb.set_trace()

def main():
    basedir = '/Volumes/ABCDrive1/submission_14921'   
    workdir = '/Users/nibl/Desktop/workit/'
    cor_maker(basedir, workdir)
main()