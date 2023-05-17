#!/bin/bash

# Taken from:
#     https://linuxconfig.org/how-to-obtain-sunrise-sunset-time-for-any-location-from-linux-command-line
#
# First obtain a location code from: https://weather.codes/search/

# Insert your location. For example LOXX0001 is a location code for Bratislava, Slovakia
location="UKXX0052"
tmpfile=/tmp/$location.out

# Obtain sunrise and sunset raw data from weather.com
wget -q "https://weather.com/weather/today/l/$location" -O "$tmpfile"

SUNR=$(grep SunriseSunset "$tmpfile" | grep -oE '((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))' | head -1)
SUNS=$(grep SunriseSunset "$tmpfile" | grep -oE '((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))' | tail -1)


sunrise=$(date --date="$SUNR" +%R)
sunset=$(date --date="$SUNS" +%R)

# Use $sunrise and $sunset variables to fit your needs. Example:
echo "Sunrise for location $location: $sunrise"
echo "Sunset for location $location: $sunset"
