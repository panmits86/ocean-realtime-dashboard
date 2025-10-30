#!/bin/bash

#Download the gfs atmospheric fields from aws
# It's manual process:
# 0. The user has to install the aws lib 
# 1. The user has to update the date_start, date_end and the dir_gfs variable where the data to be saved

#set -ex
date_start=$1  # example: date_start=20250113
date_end=$2    # example: date_end=20250114

cdate=$date_start; export cdate

# dir_gfs = the main directory where the GFS data will be saved
dir_gfs=$3 # example: dir_gfs='/media/pm/Data/Data/WaveDA/DA/ModelData/gfs_atmos'
dir_date=$dir_gfs'/'$cdate; export dir_date

while [[ $cdate -le $date_end ]]; do
# main loop: download gfs data for each cdate (dates), and cycle (t00z, t01z, t02z...) and forecast hours (f000 only)
# save the files and organize them to a directory based on date
	mkdir -p $dir_date
	#cd $dir_date
	aws s3 sync --no-sign-request s3://noaa-gfs-bdp-pds/gfs.$cdate/ $dir_gfs'/'$cdate --exclude "*" --include "*/atmos/gfs.t*z.pgrb2.0p25.f000"
	for cyc in 00 06 12 18; do
            cycle=$cyc; export cycle
            mkdir -p $dir_gfs"/gfs.t"$cyc"z.pgrb2.0p25.f000"
	    #mkdir -p $dir_gefs"/gefs.urmagrid."$cdate".t"$cyc"z.f"$fcst
            mv "$dir_gfs"/"$cdate"/"$cyc"/atmos/gfs.t"$cyc"z.pgrb2.0p25.f000"" $dir_gfs"/gfs.t"$cyc"z.pgrb2.0p25.f000/"
            dir_gfs_subset=$dir_gfs"/gfs.t"$cyc"z.pgrb2.0p25.f000/"; export dir_gfs_subset
            python3 gfs_download.py gfs_dl
        done
        
	cdate=$(date -d "$cdate + 1 day" +%Y%m%d)
	
done
