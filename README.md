## Timelapse

A shell script to create a Timelapse video.

The program takes into account sunrise and sunset times so (most) dark images will not now be 
used although there is an option to override this.

## Requirements

* Python 3.6.*
* pip
* ffmpeg (<https://github.com/FFmpeg/FFmpeg>)
* astral (https://pypi.org/project/astral/)

## Install

```bash
pip install -r requirements.txt
```

## Usage
```bash
usage: timelapse.py [-h] [--debug] [--date DATE] [--full] [--base BASE] [--output OUTPUT]

Timelapse video generator

### Arguments

```bash
  -h, --help       show this help message and exit
  --debug          Enable debug output
  --date DATE      Date to process in YYYY-MM-DD format (default: yesterday)
  --full           Generate full-day video
  --base BASE      Base directory for timelapse images
  --output OUTPUT  Output directory for timelapse videos
```


