#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   hcp_fix - wrapper script for FIX, for HCP pipelines
#    Updated grace shearrer
#
#   Stephen Smith, FMRIB Analysis Group
#
#   Copyright (C) 2012-2013 University of Oxford
#
#   SHCOPYRIGHT
#
#   Changes by Timothy B. Brown <tbbrown@wustl.edu>
#
#   1) Changes to support 7T ICAFIX processing based on changes originally made by Keith jamison <kjamison@umn.edu>
#   2) Changes to echo output messages to aid in debugging 
#   3) Changes to call version 3.14a of melodic instead of melodic in FSL distribution based on changes
#      originally made by Mohana Ramaratnam <mohanakannan9@gmail.com>

# Set this before calling hcp_fix instead, to make it more flexible
#FSL_FIXDIR=$( cd $(dirname $0) ; pwd)
#export FSL_FIXDIR

# All fix settings are held in the settings.sh file - edit this file to suit your setup
import os 
import subprocess
import glob
import pdb
import argparse
import shutil
#. ${FSL_FIXDIR}/settings.sh

#############################################################

#DEBUG="TRUE"
#
#Debug() {
#	msg="${1}"
#	if [ "${DEBUG}" = "TRUE" ]; then
#		echo "hcp_fix: DEBUG: ${msg}"
#	fi
#}
#
#Inform() {
#	msg="${1}"
#	echo "hcp_fix: INFORM: ${msg}"
#}
#
#Error() {
#	msg="${1}"
#	echo "hcp_fix: ERROR: ${msg}"
#}

def melodic_fix(basedir,arglist,fslbase):
    print('hi')
    for scan in glob.glob(os.path.join(basedir, 'sub-*','ses-baselineYear1Arm1','func','*rest*_bold.nii')):
        sub=scan.split('/')[8].split('_')[0]
        run=scan.split('/')[8].split('_')[3]
        print('this is the sub %s this is the run %s'%(sub,run))
        '''
        get TRs
        '''
        fslval = os.path.join(fslbase,'fslval')
        tr_call = '%s %s %s'%(fslval, scan, 'pixdim4')
        tr_call = tr_call.split(' ')
        print(tr_call)        

        tr = subprocess.check_output(tr_call)
        tr = float(tr)
        print(tr)
        ica_path = os.path.join(basedir,sub,'%s.ica'%run)
        print(ica_path)
        '''
        start melodic
        '''
        if os.path.exists(os.path.join(ica_path)) == True:
            print('already exists, skipping')
        else:
            os.mkdir(ica_path)
            melodic_call = '%smelodic -i %s -o %s/filtered_func_data.ica -d -250 --report --Oall --tr=%f'%(fslbase,scan,ica_path, tr)
            melodic_call = melodic_call.split(' ')
            print(melodic_call)
            subprocess.call(melodic_call)
            
        '''
        moving motion parameters
        '''
        mc_path = os.path.join(ica_path, 'mc')
        if os.path.exists(os.path.join(mc_path)):
            print('exists skip')
        else:
            os.mkdir(mc_path)
            par_path = os.path.join(mc_path,'motion.par')
            motion_file = os.path.join(basedir, 'sub-*','ses-baselineYear1Arm1','func','%s_ses-baselineYear1Arm1_task-rest_%s_motion.tsv'%(sub,run))
            mc_call = "cat %s | awk '{ print $3 " " $4 " " $2 " " $6 " " $7 " " $5}' > %s"%(motion_file, par_path)
            print(mc_call)
            subprocess.call(mc_call,shell =True)
        '''
        move stuf
        '''
	reg_path = os.path.join(ica_path,'reg')
	if os.path.exists(reg_path):
		print('already moved the registrations')
	else:
		T1_scan='%s_ses-baselineYear1Arm1_T1w.nii'%sub
		T1_path = os.path.join(basedir,sub,'ses-baselineYear1Arm1','anat',T1_scan)
		T1_new_path = os.path.join(reg_path,T1_scan)
		shutil.copyfile(T1_path, T1_new_path)
		if os.path.exists(T1_path) == True:
			T1_new_path = os.path.join(reg_path,T1_scan)
			shutil.copyfile(T1_path, T1_new_path)
		Mean_func_path = os.path.join(ica_path,'mean_func.nii.gz')
		Example_func_path = os.path.join(reg_path, 'example_func.nii.gz')
		'''
		decision point what reg do you want
		'''
	
#        $FSLDIR/bin/imln ../../../../T1w_restore_brain highres
#        $FSLDIR/bin/imln ../../../../wmparc wmparc
#        $FSLDIR/bin/imln ../mean_func example_func
#        $FSLDIR/bin/makerot --theta=0 > highres2example_func.mat
#        $FSLDIR/bin/fslmaths ../../../../T1w -div ../../../../T2w veins -odt float
#        $FSLDIR/bin/fslmaths veins -div `$FSLDIR/bin/fslstats veins -k ${FSL_FIXDIR}/mask_files/hcp_0.7mm_brain_mask -P 50` -mul 2.18 -thr 10 -min 50 -div 50 veins
#        $FSLDIR/bin/flirt -in veins -ref example_func -applyxfm -init highres2example_func.mat -out veins_exf
#        $FSLDIR/bin/fslmaths veins_exf -mas example_func veins_exf
        '''
        starting fix?
        '''
#        if arglist['FIX'] == False:
#            print('looks like there is no training file, please give a training file')
#        else:
#		print('cool')
            
#        if [ "X${TrainingData}" != X ]; then
#	# User has specified a training data file
#
#	# add .RData suffix if not already there
#	if [[ "${TrainingData}" != *.RData ]]; then 
#		TrainingData=${TrainingData}.RData
#	fi
#
#	# if the specified TrainingData is not a full path to an existing file,
#	# assume that the user is specifying the name of a file in the training_files folder in FSL_FIXDIR
#	if [ ! -f "${TrainingData}" ]; then 
#		TrainingData=${FSL_FIXDIR}/training_files/${TrainingData}
#	fi
#
#	# finally, if the TrainingData file is not found, report an error and get out of here
#	if [ ! -f "${TrainingData}" ]; then
#		Error "FIX training data not found: ${TrainingData}"
#		exit -1
#	fi
#
#	# now run fix
#	Inform "About to run: ${FSL_FIXDIR}/fix ${fmri}.ica ${TrainingData} 10 -m -h $hp"
#	${FSL_FIXDIR}/fix ${fmri}.ica ${TrainingData} 10 -m -h $hp
#
#else
#	# user has not specified a training data file
#	if [ $hp != 2000 ] ; then
#		Debug "since specified hp value (${hp}) is not 2000, we assume a value of 200"
#		Inform "About to run: ${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp200.RData 10 -m -h 200"
#		${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp200.RData 10 -m -h 200
#	else
#		Inform "About to run: ${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp2000.RData 10 -m -h 2000"
#		${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp2000.RData 10 -m -h 2000


    
def main():
    basedir = '/projects/niblab/data/ABCD/'
    fslbase = '/projects/niblab/modules/software/fsl/5.0.10/bin/'
    
    parser=argparse.ArgumentParser(description='preprocessing')
    parser.add_argument('-training',dest='TRAIN',
                        default=False, help='do we have training data already?')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    print(arglist)
    #####################################
    melodic_fix(basedir,arglist,fslbase)
    #####################################
main()  
'''
Usage() {
    cat <<EOF

hcp_fix <4D_FMRI_data> <highpass> [<TrainingFile>] #here i don't think you need the highpass
  with <highpass> being the temporal highpass full-width (2*sigma) in seconds

e.g.   hcp_fix BOLD_REST1_RL/BOLD_REST1_RL.nii.gz 200

for detrending-like behaviour, set <highpass> to 2000

EOF
    exit 1
}
[ "$2" = "" ] && Usage
'''

#
#fmri=$1
#cd `dirname $fmri`
#fmri=`basename $fmri`
#fmri=`$FSLDIR/bin/imglob $fmri`
#[ `imtest $fmri` != 1 ] && echo No valid 4D_FMRI input file specified && exit 1
#fmri_orig=$fmri
#
#hp=$2
#
#unset TrainingData
#if [ $# -ge 3 ]; then
#	TrainingData=$3
#fi
#
#tr=`$FSLDIR/bin/fslval $fmri pixdim4`
#
#Inform "processing FMRI file $fmri with highpass $hp"
#
#if [ $hp -gt 0 ] ; then
#  Inform "running highpass"
#  hptr=`echo "10 k $hp 2 / $tr / p" | dc -`
#  ${FSLDIR}/bin/fslmaths $fmri -bptf $hptr -1 ${fmri}_hp$hp
#  fmri=${fmri}_hp$hp
#fi
#################################################################
'''
Inform "running MELODIC"
mkdir -p ${fmri}.ica
Debug "About to run melodic: Contents of ${fmri}.ica follow"
if [ "${DEBUG}" = "TRUE" ] ; then
	ls -lRa ${fmri}.ica
fi

Debug "Modified version of melodic in use"
Debug "melodic located at: ${HOME}/pipeline_tools/fix1.06a/melodic used"
Debug "instead of melodic located at: ${FSLDIR}/bin/melodic"
Debug "Beginning of melodic version log"
if [ "${DEBUG}" = "TRUE" ] ; then
	${HOME}/pipeline_tools/fix1.06a/melodic --version
fi
Debug "End of melodic version log"

# "old" melodic command
#$FSLDIR/bin/melodic -i $fmri -o ${fmri}.ica/filtered_func_data.ica -d -250 --nobet --report --Oall --tr=$tr
#
${HOME}/pipeline_tools/fix1.06a/melodic -i $fmri -o ${fmri}.ica/filtered_func_data.ica -d -250 --nobet --report --Oall --tr=$tr
retCode=$?
Debug "melodic has been run: retCode = ${retCode}"
Debug "melodic has been run: Contents of ${fmri}.ica follow"
if [ "${DEBUG}" = "TRUE" ] ; then
	ls -lRa ${fmri}.ica
fi

if [ "${retCode}" -ne "0" ] ; then
    Error "melodic has returned a non-zero code"
	Error "Exiting this script with -1 return value."
	exit -1
fi

cd ${fmri}.ica

$FSLDIR/bin/imln ../$fmri filtered_func_data
$FSLDIR/bin/imln filtered_func_data.ica/mask mask

if [ `$FSLDIR/bin/imtest ../${fmri_orig}_SBRef` = 1 ] ; then
  $FSLDIR/bin/imln ../${fmri_orig}_SBRef mean_func
else
  $FSLDIR/bin/imln filtered_func_data.ica/mean mean_func
fi

if [ -f ../${fmri_orig}_Atlas.dtseries.nii ] ; then
  $FSLDIR/bin/imln ../${fmri_orig}_Atlas.dtseries.nii Atlas.dtseries.nii
fi

#mkdir -p mc
#if [ -f ../Movement_Regressors.txt ] ; then
#  cat ../Movement_Regressors.txt | awk '{ print $2 " " $3 " " $2 " " $6 " " $2 " " $5}' > mc/prefiltered_func_data_mcf.par
#else
#  Error "Movement_Regressors.txt not retrieved properly." 
#  exit -1
fi 
1           2      3         4          5        6        7
t_indx	rot_z	rot_x	rot_y	trans_z	trans_x	trans_y

Inform "functionmotionconfounds log file is to be named: .fix.functionmotionconfounds.log instead of .fix.log"
#${FSL_FIXDIR}/call_matlab.sh -l .fix.log -f functionmotionconfounds $tr $hp 
${FSL_FIXDIR}/call_matlab.sh -l .fix.functionmotionconfounds.log -f functionmotionconfounds $tr $hp 


mkdir -p reg
cd reg

i_am_at=`pwd`
Debug "current folder ${i_am_at}"

$FSLDIR/bin/imln ../../../../T1w_restore_brain highres
$FSLDIR/bin/imln ../../../../wmparc wmparc
$FSLDIR/bin/imln ../mean_func example_func
$FSLDIR/bin/makerot --theta=0 > highres2example_func.mat
$FSLDIR/bin/fslmaths ../../../../T1w -div ../../../../T2w veins -odt float
$FSLDIR/bin/fslmaths veins -div `$FSLDIR/bin/fslstats veins -k ${FSL_FIXDIR}/mask_files/hcp_0.7mm_brain_mask -P 50` -mul 2.18 -thr 10 -min 50 -div 50 veins
$FSLDIR/bin/flirt -in veins -ref example_func -applyxfm -init highres2example_func.mat -out veins_exf
$FSLDIR/bin/fslmaths veins_exf -mas example_func veins_exf
cd ../..

Inform "running FIX"

# Changes to handle user specified training data file
if [ "X${TrainingData}" != X ]; then
	# User has specified a training data file

	# add .RData suffix if not already there
	if [[ "${TrainingData}" != *.RData ]]; then 
		TrainingData=${TrainingData}.RData
	fi

	# if the specified TrainingData is not a full path to an existing file,
	# assume that the user is specifying the name of a file in the training_files folder in FSL_FIXDIR
	if [ ! -f "${TrainingData}" ]; then 
		TrainingData=${FSL_FIXDIR}/training_files/${TrainingData}
	fi

	# finally, if the TrainingData file is not found, report an error and get out of here
	if [ ! -f "${TrainingData}" ]; then
		Error "FIX training data not found: ${TrainingData}"
		exit -1
	fi

	# now run fix
	Inform "About to run: ${FSL_FIXDIR}/fix ${fmri}.ica ${TrainingData} 10 -m -h $hp"
	${FSL_FIXDIR}/fix ${fmri}.ica ${TrainingData} 10 -m -h $hp

else
	# user has not specified a training data file
	if [ $hp != 2000 ] ; then
		Debug "since specified hp value (${hp}) is not 2000, we assume a value of 200"
		Inform "About to run: ${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp200.RData 10 -m -h 200"
		${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp200.RData 10 -m -h 200
	else
		Inform "About to run: ${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp2000.RData 10 -m -h 2000"
		${FSL_FIXDIR}/fix ${fmri}.ica ${FSL_FIXDIR}/training_files/HCP_hp2000.RData 10 -m -h 2000
	fi

fi

$FSLDIR/bin/immv ${fmri}.ica/filtered_func_data_clean ${fmri}_clean

if [ -f ${fmri}.ica/Atlas_clean.dtseries.nii ] ; then
  /bin/mv ${fmri}.ica/Atlas_clean.dtseries.nii ${fmri_orig}_Atlas_hp${hp}_clean.dtseries.nii
fi
'''
