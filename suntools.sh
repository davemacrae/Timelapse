#!/bin/bash
#set -o errexit -o pipefail -o noclobber -o nounset

#########################################################################
#   Enter your location ID - find it on https://weather.codes/search/   #
    location=UKXX0052
#########################################################################

# get script filename with which it was invoked
sf=`basename "$0"`

q=false
qq=false
jr=true # Both $jr and $js are true by default
js=true # The switches then turn off the opposite

DEBUG=false # set value to `true` in order to debug getopts

while getopts "rsqwhvel:" opt; do
    case $opt in
q)
    q=true
[ $DEBUG = "true" ] && echo "-q"
;;

w)
    qq=true
[ $DEBUG = "true" ] && echo "-w"
;;

l)
    location=$OPTARG
[ $DEBUG = "true" ] && echo "-l $location"
;;

r)
    js=false
[ $DEBUG = "true" ] && echo "-r"
;;

s)
    jr=false
[ $DEBUG = "true" ] && echo "-s"
;;
h)
    printf "Welcome to Bash SunTools!\nSimply enter your location ID (which you can obtain from https://weather.codes/search/) into the script and voila!\n\n"
    echo "no parameters: both sunrise and sunset"
    echo "-r    Fetch sunrise for your entered location from weather.com"
    echo "-s    Fetch sunset for your entered location from weather.com"
    echo "-q    Be quiet"
    echo "-w    Even quieter"
    echo "-l X  Specify location ID"
    echo "-h    Print this message and exit"
    echo "-v    Print script version number and exit"
    echo " "
    echo "Examples: "
    echo "$sf -rwl USNY0996     Get the sunrise time in New York in HHMM format"
    echo "$sf -sl ITXX0067      Get the sunset time in Rome"
    echo " "
    echo "Disclaimer: This script does NOT contain any easter eggs."
    exit
;;

v)
    echo "SunTools by @ZeevoX - v1.0"
    exit
;;

e)
if ! [ -x "$(command -v cowsay)" ]; then
    echo 'There is nothing to see here. Ew.'
    exit
else
    cowsay "SunTools!"
    echo "Note that this is a developer debugging feature, NOT AN EASTER EGG."
    echo "__ moo __"
    exit
fi
;;

\?)
    echo "Handle error: unknown option or missing required argument."
    exit
;;
    esac
done

# check that lynx is installed
if ! [ -x "$(command -v lynx)" ]; then
    printf 'Error: lynx is not installed. Install it with\n\n\tsudo apt install lynx\n\nAborting script.\n'
    exit 1
fi

# Obtain sunrise and sunset raw data from weather.com
sun_times=$( lynx --dump  https://weather.com/weather/today/l/$location | grep "\* Sun" | sed "s/[[:alpha:]]//g;s/*//" )
# Extract sunrise and sunset times and convert to 24 hour format
if [ $qq == "true" ] ; then
    sunrise=$(date --date="`echo $sun_times | awk '{ print $1}'` AM" +%H%M)
    sunset=$(date --date="`echo $sun_times | awk '{ print $2}'` PM" +%H%M)
else
    sunrise=$(date --date="`echo $sun_times | awk '{ print $1}'` AM" +%R)
    sunset=$(date --date="`echo $sun_times | awk '{ print $2}'` PM" +%R)
fi

if [ $q == "true" ] || [ $qq == "true" ] ; then
    e_sunrise="$sunrise"
    e_sunset="$sunset"
else
    e_sunrise="Sunrise will be at $sunrise"
    e_sunset="Sunset will be at $sunset"
fi

if [ $jr == $js ] ; then # show sunset AND sunrise when either both parameters passed or by default
    echo $e_sunrise
    echo $e_sunset
elif [ $jr == "true" ] ; then
    echo $e_sunrise
elif [ $js == "true" ] ; then
    echo $e_sunset
fi
