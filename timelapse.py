#!/usr/bin/env python
'''
Module: timelapse
Description: This module gathers image files taken between dawn and dusk for a given date
             and generates a timelapse video script. It thenb rus ffmpwg to create the video.

    TODO: Handle cases where no files are found between dawn and dusk.
    TODO: Add error handling for subprocess calls.
    DONE: Add argument parsing to specify date.
    DONE: Add debug argument to toggle debug prints.
    DONE: Make a shorter version of the video for quick viewing.

'''
from sun import get_sun_data
from datetime import datetime, timedelta
import subprocess
import shlex
from pathlib import Path
import argparse

CITY_NAME = "Edinburgh"
# BASE = "/home/dave/src/Timelapse/Timelapse/"
BASE = "/backup/DCIM/Timelapse/"

def arg_parser() -> argparse.Namespace:

    ''' Process the command line arguments '''

    parser = argparse.ArgumentParser(description="Timelapse video generator")
    parser.add_argument('--debug', action="store_true", help="Enable debug output")
    parser.add_argument('--date', type=str, help="Date to process in YYYY-MM-DD format (default: yesterday)")

    return parser.parse_args()

def gather_files (date_time) -> list:
    ''' Gather files between start and finish times for timelapse processing. '''
    # Calculate the time of Dusk and Dawn for date_time
    
    sun_data = get_sun_data(CITY_NAME, date_time)
    if args.debug:
        print(f"Sun data in {CITY_NAME} on {date_time}:")
        print(f"Dawn: {sun_data['dawn']}")
        print(f"Sunrise: {sun_data['sunrise']}")
        print(f"Sunset: {sun_data['sunset']}")
        print(f"Dusk: {sun_data['dusk']}")
        print(f"Process from {sun_data['dawn'].hour}:{sun_data['dawn'].minute} to {sun_data['dusk'].hour}:{sun_data['dusk'].minute} for timelapse photography.")

    first_hour = sun_data['dawn'].hour
    last_hour = sun_data['dusk'].hour
    first_minute = sun_data['dawn'].minute
    last_minute = sun_data['dusk'].minute

    base_day = date_time.strftime("%Y-%m-%d")

    file_list = []

    # iterate through BASE/first to BASE/last
    # We need partial extraction from DASE/first and BASE/last but full extraction from BASE/first+1 to BASE/last-1
    # e.g. if first is 06:15 and last is 18:45
    # we need BASE/06 from 15 mins, BASE/07 to BASE/17 fully, and BASE/18 to 45 mins
    for hour in range(first_hour, last_hour + 1):
        hour_str = f"{hour:02d}"
        dir_path = BASE + base_day + "/" + hour_str + "/"
        if hour == first_hour:
            start_minute = first_minute
        else:
            start_minute = 0
        if hour == last_hour:
            end_minute = last_minute
        else:
            end_minute = 59
        for minute in range(start_minute, end_minute + 1):
            minute_str = f"{minute:02d}"
            file_path = dir_path + base_day + "_" + hour_str + "-" + minute_str + "-*_001.jpg"
            f = Path(dir_path)
            glob_path = base_day + "_" + hour_str + "-" + minute_str + "-*_001.jpg"
            f = f.glob(glob_path)
            if args.debug:
                for i in f:
                    print(f"{i.parent}/{i.name}" )
                print(f"Gathering file: {file_path}")
            # Here you would add code to actually process the file 
            for i in f:
                if i.stat().st_size > 0:
                    file_list.append(f"{i.parent}/{i.name}")

    return(file_list)

def gen_script(file_list, date_time, duration) -> None:
    ''' Generate a script to process the gathered files into a timelapse video. '''
    day = date_time.strftime("%Y-%m-%d")
    script_name = f"{day}.script"
    with open(script_name, 'w') as script_file:
        for file in file_list:
            script_file.write(f"file '{file}'\n")
            script_file.write(f"duration {duration}\n")
    if args.debug:
        print(f"Generated script: {script_name}")

    script = f"ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i {script_name} -fps_mode vfr -c:v libx265 -pix_fmt yuv420p -x265-params log-level=quiet {day}-{duration}.mkv"
    ffmpeg = shlex.split(script)
    p = subprocess.Popen(ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    if p.returncode != 0:
        print(f'Command {p.args} exited with {p.returncode} code, output: \n{p.stdout}')

def main() -> None:
    ''' Main function to gather files and generate timelapse videos. '''
    # Determine the date to process
    if args.date:
        date_time = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date_time = datetime.now() - timedelta(days=1)
    files = gather_files(date_time)
    gen_script(files, date_time, duration=0.25)
    gen_script(files, date_time, duration=0.05)

if __name__ == "__main__":

    args = arg_parser()
    main()
