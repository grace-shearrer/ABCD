library("dplyr")
library("plyr")
library("psych")
random <-read.table('~/Google Drive/ABCD/important_txt/female_puberty_ana.csv',sep=",", header=T)
head(random)
real<-read.table("~/Google Drive/ABCD/important_txt/female_data.csv", sep=",", header=T)
head(real)

all<-join(random, real)
names(all)
write.table(all, "~/Google Drive/ABCD/important_txt/comb_female.csv", sep=",", row.names = F)


QC <- read.table("~/Google Drive/ABCD/important_txt/mriqc01.csv", sep=",", header=T)
names(QC)
QCvars<-c("collection_id","dataset_id", "subjectkey", "src_subject_id",                
          "interview_date","interview_age","gender","visit",
          "iqc_t1_1_qc_score", "iqc_t1_1_complete","iqc_t1_2_qc_score","iqc_t1_2_pc_score",
          "iqc_t1_2_complete","iqc_t1_3_qc_score","iqc_t1_3_pc_score","iqc_t1_3_complete",
          "iqc_rsfmri_1_fm_qc_score", "iqc_rsfmri_1_fm_pc_score","iqc_rsfmri_1_qc_score",
          "iqc_rsfmri_1_pc_score","iqc_rsfmri_1_complete", "iqc_rsfmri_2_fm_qc_score",
          "iqc_rsfmri_2_fm_pc_score","iqc_rsfmri_2_qc_score","iqc_rsfmri_3_fm_qc_score",
          "iqc_rsfmri_3_fm_pc_score","iqc_rsfmri_3_qc_score","iqc_rsfmri_3_pc_score",
          "iqc_rsfmri_4_fm_qc_score", "iqc_rsfmri_4_fm_pc_score", "iqc_rsfmri_4_fm_complete",
          "iqc_rsfmri_4_qc_score", "iqc_rsfmri_4_pc_score", "iqc_rsfmri_5_fm_pc_score", "iqc_rsfmri_5_qc_score",
          "iqc_rsfmri_5_pc_score", "iqc_rsfmri_6_fm_qc_score", "iqc_rsfmri_6_fm_pc_score","iqc_rsfmri_6_qc_score",
          "iqc_rsfmri_6_pc_score","iqc_rsfmri_7_fm_qc_score","iqc_rsfmri_7_fm_pc_score","iqc_rsfmri_7_fm_complete",
          "iqc_rsfmri_7_qc_score", "iqc_rsfmri_7_pc_score","iqc_rsfmri_8_qc_score", "iqc_rsfmri_8_pc_score",
          "iqc_rsfmri_9_fm_qc_score","iqc_rsfmri_9_fm_pc_score","iqc_rsfmri_9_qc_score","iqc_rsfmri_9_pc_score",
          "iqc_rsfmri_10_fm_qc_score","iqc_rsfmri_10_fm_pc_score","iqc_rsfmri_10_qc_score","iqc_rsfmri_10_pc_score"
          )

qc<-QC[QCvars]
names(qc)
describe(qc)

names(all)
dataT1 <- subset(all, all$session_det == "ABCD-MPROC-T1")
dataRest <- subset(all, all$session_det == "ABCD-MPROC-rest")
head(dataT1)
head(dataRest)

myvars <- c("src_subject_id","derived_files")
T1 <- dataT1[myvars]
head(T1)

myvars <- c("src_subject_id","derived_files")
rest <- dataRest[myvars]
head(rest)

scans<-join(T1, rest)
dim(T1)

write.table(T1, "~/Google Drive/ABCD/important_txt/T1_female.csv", sep=",", row.names = F)
write.table(rest, "~/Google Drive/ABCD/important_txt/Rest_female.csv", sep=",", row.names = F)
write.table(scans, "~/Google Drive/ABCD/important_txt/Scans_female.csv", sep=",", row.names = F)

