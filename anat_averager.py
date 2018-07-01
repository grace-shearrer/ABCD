import os
import subprocess
import glob

def anatomical_ave(basedir):
        for scan in glob.glob(os.path.join(basedir, 'sub-*','ses-baselineYear1Arm1','anat')):
                print(scan)
                sub=scan.split('/')[5]
                T1scans = glob.glob(os.path.join(scan,'*T1w*.nii'))
                T2scans = glob.glob(os.path.join(scan,'*T2w*.nii'))
		'''
		if len(T1scans) > 1:
			output = os.path.join(scan,'averageT1')
			if os.path.exists(output):
				print('%s exists skipping')
			else:
				call = 'AnatomicalAverage %s %s -o %s -v -w %s'%(T1scans[0], T1scans[1],output,scan)
				call_run = subprocess.Popen(call, shell=True)
				call_run.wait()
		if len(T2scans) > 1:
			output = os.path.join(scan,'averageT2')
			if os.path.exists(output): 
				print('%s exists skipping'%s)
			else:
				call = 'AnatomicalAverage %s %s -o %s -v -w %s'%(T2scans[0], T2scans[1],output,scan)
				call_run = subprocess.Popen(call, shell=True)
				call_run.wait()
		'''
		ref='/projects/niblab/modules/software/fsl/5.0.10/data/standard/MNI152_T1_2mm.nii.gz'
		print('starting ACPC alignment :D ')
		allT1 = glob.glob(os.path.join(scan,'*T1w*.nii'))
		allT2 = glob.glob(os.path.join(scan,'*T2w*.nii'))
		if len(allT1) < 2:
			for image in T1scans:
				print(image)
				output = os.path.join(scan,'averageT1')
				output = '%s_ACPC'%output
				print(output)
				if os.path.exists(output):
					print('%s already aligned'%output)
				else:
					ACPC = '/projects/niblab/scripts/ABCD/ABCD/ACPCAlignment.sh --workingdir=%s --in=%s --ref=%s --out=%s --omat=%s'%(scan,image,ref,output,output)
					ACPC_run = subprocess.Popen(ACPC, shell = True)
					ACPC_run.wait()
		if len(allT1) > 2:
			for image in T1scans:
				print(image)
				output = image.split('.')[0]
				output = '%s_ACPC'%output
				print(output)
				if os.path.exists(output):
					print('%s already aligned'%output)
				else:
					ACPC = '/projects/niblab/scripts/ABCD/ABCD/ACPCAlignment.sh --workingdir=%s --in=%s --ref=%s --out=%s --omat=%s'%(scan,image,ref,output,output)
					ACPC_run = subprocess.Popen(ACPC, shell = True)
					ACPC_run.wait()	
def main():
	basedir = '/projects/niblab/data/ABCD/'
	anatomical_ave(basedir)
main()
