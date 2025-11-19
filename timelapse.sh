#!/bin/sh

DAY=$(date --date=yesterday +%Y-%m-%d)
DIR=/home/dave/src/Timelapse

cd ${DIR}

# Copy the files over

# scp -r root@neos-con:/system/sdcard/DCIM/Timelapse/${DAY} Timelapse
cp -r /backup/DCIM/Timelapse/${DAY} Timelapse

# remove the files

# ssh root@neos-con "rm -rf /system/sdcard/DCIM/Timelapse/${DAY}"

rm -f ${DAY}.script
rm -f ${DAY}.mp4

# We really need to get the deatils of sunrise and sunset so we can filter out the darkness from the images.
for i in $(find Timelapse/${DAY} ! -type d ! -size 0 | sort) 
do 
    echo "file '${i}'" >> ${DAY}.script
    echo duration 0.25 >> ${DAY}.script
done
echo "file '${i}'" >> ${DAY}.script

ffmpeg -loglevel error -safe 0 -f concat -i ${DAY}.script -vsync vfr -pix_fmt yuv420p ${DAY}.mp4

rm -f ${DAY}.script
