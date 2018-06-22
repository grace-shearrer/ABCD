#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 15:13:02 2018

@author: gracer
"""

import os
import pandas as pd
import glob
from nda_aws_token_generator import *
import awsdownload
import subprocess

colnames = ['sub', 'scan']

basedir = '/Users/gracer/Google Drive/ABCD/important_txt/female_scans'

for txtfile in glob.glob(os.path.join(basedir,'*.csv')):
    infile = pd.read_csv(txtfile, names=colnames)
    scans = infile.scan.tolist()
    print(scans)
    for item in scans:
        call = "python awsdownload.py %s -r -u args['WHO'] -p args['SECRET']"
        subprocess.call
#names = data.name.tolist()
#latitude = data.latitude.tolist()
#longitude = data.longitude.tolist()
        
# make main and func, have to pass username and password