import os
import subprocess
import pdb
import glob
########################################## DO WORK ########################################## 
def BET(basedir,fslbase,reference2mm, referencemask2mm,reference0_7mm,outputmask,output):
	for scan in glob.glob(os.path.join(basedir, 'sub-*','ses-baselineYear1Arm1','anat')):
		print(scan)
		all_ACPC = glob.glob(os.path.join(scan,'average*_ACPC.nii.gz'))
        	for item in all_ACPC:
			item = item.split('.')[0]
			flirt = '%sflirt -interp spline -dof 12 -in %s -ref %s -omat %s_toMRIrough.mat -out %s_to_MNI_roughlin.nii.gz -nosearch -v'%(fslbase,item, reference2mm, item, item)
			fnirt = '%sfnirt --in=%s --ref=%s --aff=%s_toMRIrough.mat --refmask=%s --fout=%s_str2standard.nii.gz --jout=%s_NonlinearRegJacobians.nii.gz --refout=%s_IntensityModulatedT1.nii.gz --iout=%s_to_MNI_nonlin.nii.gz --logout=%s_NonlinearReg.txt --intout=%s_NonlinearIntensities.nii.gz --cout=%s_NonlinearReg.nii.gz'%(fslbase,item,reference2mm,item, referencemask2mm,item,item,item,item,item,item, item)
			highwarp = '%sapplywarp --rel --interp=spline --in=%s --ref=%s -w %s_str2standard.nii.gz --out=%s_to_MNI_nonlin.nii.gz'%(fslbase,item, reference0_7mm,item, item)
			in_warp='%sinvwarp --ref=%s -w %s_str2standard.nii.gz -o %s_standard2str.nii.gz'%(fslbase, reference2mm, item, item)
			print(in_warp)
			apply_warp='%sapplywarp --rel --interp=nn --in=%s --ref=%s -w %s_standard2str.nii.gz -o %s_%s'%(fslbase,referencemask2mm, item, item, item,outputmask)
			maths = '%sfslmaths %s -mas %s_%s %s%s'%(fslbase,item, item, outputmask,item, output)
			if os.path.exists('%s_to_MNI_roughlin.nii.gz'%item):	
				print('skipping flirt')
			else:
				flirt_run=subprocess.Popen(flirt, shell =True)
				flirt_run.wait()
			if os.path.exists('%s_NonlinearIntensities.nii.gz'%item):
				print('fnirt exists skipping')
			else:
				fnirt_run=subprocess.Popen(fnirt,shell = True)
				fnirt_run.wait()
			if os.path.exists('%s_to_MNI_nonlin.nii.gz'%item):
				print('high warp exists')
			else:
				highwarp_run=subprocess.Popen(highwarp, shell = True)
				highwarp_run.wait()
			if os.path.exists('%s_standard2str.nii.gz'%item):
				print('inverse warp done')
			else:
				invwarp_run=subprocess.Popen(in_warp, shell = True)
				invwarp_run.wait()
			if os.path.exists('%s_%s'%(item,outputmask)):
				print('final warp done')
			else:
				apply_warp_run = subprocess.Popen(apply_warp, shell = True)
				apply_warp_run.wait()
			maths_run = subprocess.Popen(maths, shell = True)
			maths_run.wait()
			pdb.set_trace()
def main():
	basedir = '/projects/niblab/data/ABCD'
	fslbase = '/projects/niblab/modules/software/fsl/5.0.10/bin/'
	reference2mm = '/projects/niblab/data/ABCD/templates/MNI152_T1_2mm.nii.gz'
	referencemask2mm = '/projects/niblab/modules/software/fsl/5.0.10/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'
	reference0_7mm = '/projects/niblab/data/ABCD/templates/MNI152_T1_0.7mm_brain.nii.gz'
	outputmask = 'FINALmask'
	output = '_brain'
	BET(basedir,fslbase,reference2mm, referencemask2mm, reference0_7mm,outputmask, output)
main()
'''
# Register to 2mm reference image (linear then non-linear)
${FSLDIR}/bin/flirt -interp spline -dof 12 -in "$Input" -ref "$Reference2mm" -omat "$WD"/roughlin.mat -out "$WD"/"$BaseName"_to_MNI_roughlin.nii.gz -nosearch
echo "start fnirt"
${FSLDIR}/bin/fnirt --in="$Input" --ref="$Reference2mm" --aff="$WD"/roughlin.mat --refmask="$Reference2mmMask" --fout="$WD"/str2standard.nii.gz --jout="$WD"/NonlinearRegJacobians.nii.gz --refout="$WD"/IntensityModulatedT1.nii.gz --iout="$WD"/"$BaseName"_to_MNI_nonlin.nii.gz --logout="$WD"/NonlinearReg.txt --intout="$WD"/NonlinearIntensities.nii.gz --cout="$WD"/NonlinearReg.nii.gz --config="$FNIRTConfig"
echo " start apply warp"
# Overwrite the image output from FNIRT with a spline interpolated highres version
${FSLDIR}/bin/applywarp --rel --interp=spline --in="$Input" --ref="$Reference" -w "$WD"/str2standard.nii.gz --out="$WD"/"$BaseName"_to_MNI_nonlin.nii.gz
echo "inverse warp"
# Invert warp and transform dilated brain mask back into native space, and use it to mask input image
# Input and reference spaces are the same, using 2mm reference to save time
${FSLDIR}/bin/invwarp --ref="$Reference2mm" -w "$WD"/str2standard.nii.gz -o "$WD"/standard2str.nii.gz
echo " apply warp again"
${FSLDIR}/bin/applywarp --rel --interp=nn --in="$ReferenceMask" --ref="$Input" -w "$WD"/standard2str.nii.gz -o "$OutputBrainMask"
echo" maths "
${FSLDIR}/bin/fslmaths "$Input" -mas "$OutputBrainMask" "$OutputBrainExtractedImage"

echo " "
echo " END: BrainExtraction_FNIRT"
echo " END: `date`" >> $WD/log.txt

########################################## QA STUFF ########################################## 

if [ -e $WD/qa.txt ] ; then rm -f $WD/qa.txt ; fi
echo "cd `pwd`" >> $WD/qa.txt
echo "# Check that the following brain mask does not exclude any brain tissue (and is reasonably good at not including non-brain tissue outside of the immediately surrounding CSF)" >> $WD/qa.txt
echo "fslview $Input $OutputBrainMask -l Red -t 0.5" >> $WD/qa.txt
echo "# Optional debugging: linear and non-linear registration result" >> $WD/qa.txt
echo "fslview $Reference2mm $WD/${BaseName}_to_MNI_roughlin.nii.gz" >> $WD/qa.txt
echo "fslview $Reference $WD/${BaseName}_to_MNI_nonlin.nii.gz" >> $WD/qa.txt

'''
##############################################################################################
