library(plyr)
library(psych)
library(ggplot2)

PDS_score<-function(x){
  sums<-rowSums (x, na.rm = TRUE, dims = 1)
  divBy<-apply(x,1, test)
  PDSscore<-sums/divBy
  return(PDSscore)
}

test<-function(x){
  y<-sum(!is.na(x))
  return(y)
}


#load in data
setwd("/Users/gracer/Google Drive/ABCD/important_txt/")
test1<-read.table("abcd_ant01.txt", header=T, fill=T)
names(test1)
test2<-read.table("abcd_hsss01.txt", header=T, fill=T)
names(test2)
test3<-read.table("abcd_mx01.txt", header=T, fill=T)
names(test3)
test5<-read.table("abcd_ypdms01.txt", header=T, fill=T, sep="\t")
names(test5)
test6<-read.table("interview_data.txt", header=T, fill=T, sep="\t")
#join them all together
################################################################################################################################################################
data<-join(test1,test2)
names(data)
data2<-join(data,test3)
names(data2)
data3<-join(data2,test6)
data4<-join(data3,test5)
keep<-c(	"src_subject_id","interview_date",
         "interview_age","gender","anthroheightcalc","anthroweightcalc","anthro_waist_cm",
         "hormone_scr_dhea_mean","hormone_scr_hse_mean","hormone_scr_ert_mean",
         "medhx_2c","medhx_2e","medhx_2f","medhx_2g","medhx_2h","medhx_2j","medhx_2m", 
         "pds_ht2_y",	"pds_skin2_y",	"pds_bdyhair_y",	"pds_f4_2_y",	"pds_f5_y",	"pds_m4_y",	"pds_m5_y")
final_data<-data4[keep]
names(final_data)
#1/3/2017
#as.Date(x,'%m/%d/%Y')
# final_data$days_since_period<- difftime(as.Date(final_data$interview_date,'%m/%d/%Y') ,as.Date(final_data$menstrualcycle1_y,'%m/%d/%Y') , units = c("days"))
# final_data$days_since_period<-as.numeric(final_data$days_since_period)
# summary(final_data$days_since_period)
# summary(final_data$menstrualcycle1_y)

final_data$hormone_scr_dhea_mean<-as.numeric(final_data$hormone_scr_dhea_mean)
summary(final_data)
class(final_data$hormone_scr_dhea_mean)

final_data<-subset(final_data,final_data$medhx_2c == 0)
dim(final_data)
final_data<-subset(final_data,final_data$medhx_2e == 0)
dim(final_data)
final_data<-subset(final_data,final_data$medhx_2f == 0)
dim(final_data)
final_data<-subset(final_data,final_data$medhx_2g == 0)
dim(final_data)
final_data<-subset(final_data,final_data$medhx_2h == 0)
dim(final_data)
final_data<-subset(final_data,final_data$medhx_2j == 0)
dim(final_data)
final_data<-subset(final_data,final_data$medhx_2m == 0)
dim(final_data)
names(final_data)

final_data$sex[final_data$gender=="M"]<-0
final_data$sex[final_data$gender=="F"]<-1
summary(final_data)
##########
#excluding incomplete puberty data
pubSub<-c("src_subject_id","pds_ht2_y","pds_skin2_y","pds_bdyhair_y","pds_f4_2_y","pds_f5_y")
pubFem<-final_data[pubSub]
head(pubFem)
summary(pubFem)
pubFemC <- na.omit(pubFem)
pubFemC
pubFemC[!complete.cases(pubFemC),]
class(pubFemC$pds_f5_y)
pubFemC$pds_bdyhair_y<-as.integer(pubFemC$pds_bdyhair_y)

pubFemC$PDS<-PDS_score(pubFemC[2:6])
hist(pubFemC$PDS, breaks=12, col="red")
describe(pubFemC$PDS)

#excluding incomplete puberty data boy
pubSub<-c("src_subject_id","pds_ht2_y","pds_skin2_y","pds_bdyhair_y","pds_m4_y",	"pds_m5_y")
pubM<-final_data[pubSub]
head(pubM)
summary(pubM)
pubMC <- na.omit(pubM)
pubMC
pubMC[!complete.cases(pubMC),]
class(pubMC$pds_m5_y)
pubMC$pds_bdyhair_y<-as.integer(pubMC$pds_bdyhair_y)

pubMC$PDS<-PDS_score(pubMC[2:6])
hist(pubMC$PDS, breaks=12, col="red")
describe(pubMC)
#########
df <- merge(pubFemC, pubMC,by=c("src_subject_id","pds_ht2_y","pds_skin2_y","pds_bdyhair_y","PDS"), all=T)

summary(df)
#########
df2<-merge(df, final_data, by=c("src_subject_id","pds_ht2_y","pds_skin2_y","pds_bdyhair_y"))
summary(df2)
names(df2)
keep2<-c("src_subject_id","pds_ht2_y", "pds_skin2_y", "pds_bdyhair_y", "PDS", "pds_f4_2_y.x",         
         "pds_f5_y.x","pds_m4_y.x","pds_m5_y.x","interview_age","gender","anthroheightcalc",     
        "anthroweightcalc","anthro_waist_cm","hormone_scr_dhea_mean", "hormone_scr_hse_mean",  "hormone_scr_ert_mean",              
         "sex")
data<-df2[keep2]
names(data)
summary(data)

data$pds_f5_y.x[data$sex==0]<-0
data$pds_f4_2_y.x[data$sex==0]<-0
data$menstrualcycle2_y[data$sex==0]<-0
data$menstrualcycle3_y[data$sex==0]<-0
data$menstrualcycle4_y[data$sex==0]<-0
data$menstrualcycle5_y[data$sex==0]<-0
data$menstrualcycle6_y[data$sex==0]<-0

data$pds_m4_y.x[data$sex==1]<-0
data$pds_m5_y.x[data$sex==1]<-0

names(data)<-c("src_subject_id","pds_ht2_y", "pds_skin2_y", "pds_bdyhair_y", "PDS", "pds_f4_2_y",         
               "pds_f5_y","pds_m4_y","pds_m5_y","interview_age","gender","anthroheightcalc",     
               "anthroweightcalc","anthro_waist_cm","hormone_scr_dhea_mean", "hormone_scr_hse_mean",  "hormone_scr_ert_mean",              
               "sex")
write.table(data, "4Kmeans.csv", sep=",", row.names = F)
