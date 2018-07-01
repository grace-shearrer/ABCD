import os
import subprocess
import glob

def anatomical_ave(basedir):
        for scan in glob.glob(os.path.join(basedir, 'sub-*','ses-baselineYear1Arm1','anat')):
                print(scan)
                sub=scan.split('/')[5]
                T1scans = glob.glob(os.path.join(scan,'*T1w*.nii'))
                T2scans = glob.glob(os.path.join(scan,'*T2w*.nii'))
		if len(T1scans) > 1:
			output = os.path.join(scan,'averageT1')
			call = 'AnatomicalAverage %s %s -o %s -v -w %s'%(T1scans[0], T1scans[1],output,scan)
			call_run = subprocess.Popen(call, shell=True)
			call_run.wait()
def main():
	basedir = '/projects/niblab/data/ABCD/'
	anatomical_ave(basedir)
main()
