#!/usr/bin/env python3

from subprocess import run
from pathlib import Path
import typer
import time
import re
import datetime
import sys


def main(wallpaper_dir: Path):
    if not wallpaper_dir.is_dir():
        return

    current_time = datetime.datetime.now()
    current_time = (current_time.hour, current_time.minute)

    images = reversed(sorted(wallpaper_dir.iterdir()))
    for i in images:
        if match := re.match("(\d\d):(\d\d)", i.name):
            hour = int(match.group(1))
            minute = int(match.group(2))
            print(f"{i}")
            if (hour, minute) <= current_time:
                run(["plasma-apply-wallpaperimage", i.absolute()])
                return
    
    sys.stderr.write("No suitable image found\n")

if __name__ == "__main__":
    typer.run(main)