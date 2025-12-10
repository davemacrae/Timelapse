#!/usr/bin/env python
'''
Module: timelapse
Description: This module gathers image files taken between dawn and dusk for a given date
             and generates a timelapse video script. It thenb rus ffmpwg to create the video.

    DONE: Handle cases where no files are found between dawn and dusk.
    DONE: Add error handling for subprocess calls.
    DONE: Add argument parsing to specify date.
    DONE: Add debug argument to toggle debug prints.
    DONE: Make a shorter version of the video for quick viewing.
    DONE: Tidy up output files post-processing.
    TODO: Compress and remove original images after processing.

'''
from sun import get_sun_data
from datetime import datetime, timedelta
import subprocess
import shlex
from pathlib import Path
import argparse
from os import remove

CITY_NAME = "Edinburgh"
BASE = "/backup/DCIM/Timelapse"
OUTPUT = "/home/dave/Videos/Timelapse"

def arg_parser() -> argparse.Namespace:

    ''' Process the command line arguments '''

    parser = argparse.ArgumentParser(description="Timelapse video generator")
    parser.add_argument('--debug', action="store_true", help="Enable debug output")
    parser.add_argument('--date', type=str, help="Date to process in YYYY-MM-DD format (default: yesterday)")
    parser.add_argument('--full', action="store_true", help="Generate full-day video")
    parser.add_argument('--base', type=str, help="Base directory for timelapse images", default=BASE)
    parser.add_argument('--output', type=str, help="Output directory for timelapse videos", default=OUTPUT)

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

    if args.full:
        first_hour = 0
        last_hour = 23
        first_minute = 0
        last_minute = 59
    else:
        first_hour = sun_data['dawn'].hour
        last_hour = sun_data['dusk'].hour
        first_minute = sun_data['dawn'].minute
        last_minute = sun_data['dusk'].minute

    base_day = date_time.strftime("%Y-%m-%d")

    file_list = []

    # iterate through args.base/first to args.base/last
    # We need partial extraction from args.base/first and args.base/last but full extraction from args.base/first+1 to args.base/last-1
    # e.g. if first is 06:15 and last is 18:45
    # we need args.base/06 from 15 mins, args.base/07 to args.base/17 fully, and args.base/18 to 45 mins
    for hour in range(first_hour, last_hour + 1):
        hour_str = f"{hour:02d}"
        dir_path = args.base + "/" + base_day + "/" + hour_str + "/"
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
            f = Path(dir_path)
            glob_path = base_day + "_" + hour_str + "-" + minute_str + "-*_001.jpg"
            f = f.glob(glob_path)
            if args.debug:
                for i in f:
                    print(f"Gathering file: {i.parent}/{i.name}")
            for i in f:
                if i.stat().st_size > 0:
                    file_list.append(f"{i.parent}/{i.name}")

    return(file_list)

def gen_video(file_list, date_time, duration) -> None:
    ''' Generate a script to process the gathered files into a timelapse video. '''
    
    day = date_time.strftime("%Y-%m-%d")
    month = date_time.strftime("%m")
    year = date_time.strftime("%Y")
    output_dir = args.output + "/" + year + "/" + month + "/"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    out_file = output_dir + "/" + day + f"-{duration}.mp4"

    script_name = f"{day}.script"
    with open(script_name, 'w') as script_file:
        for file in file_list:
            script_file.write(f"file '{file}'\n")
            script_file.write(f"duration {duration}\n")

    script = f"ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i {script_name} -fps_mode vfr -c:v libx265 -pix_fmt yuv420p -x265-params log-level=quiet {out_file}"
    ffmpeg = shlex.split(script)
    try:
        p = subprocess.Popen(ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
    except Exception as e:
        print(f"Error executing command: {e}")
        remove(script_name) if script_name and Path(script_name).exists() else None
        remove(out_file) if Path(out_file).exists() else None
        return
    if p.returncode != 0:
        print(f'Command {p.args} exited with {p.returncode} code, output: \n{p.stdout}')

    # Tidy up script file
    script_file.close()
    remove(script_name)

def main() -> None:
    ''' Main function to gather files and generate timelapse videos. '''
    # Determine the date to process
    if args.date:
        try:
            date_time = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date or format. Please use YYYY-MM-DD.")
            return
    else:
        # Default to yesterday
        date_time = datetime.now() - timedelta(days=1)
    files = gather_files(date_time)
    if files:
        gen_video(files, date_time, duration=0.25)
        gen_video(files, date_time, duration=0.05)
    else:
        if args.debug:
            print("No files found for the specified date.")

if __name__ == "__main__":

    script_name = ""
    args = arg_parser()
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        remove(script_name) if script_name and Path(script_name).exists() else None
