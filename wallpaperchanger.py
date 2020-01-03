#!/usr/bin/env python3
"""wallpaperchanger.py - simple wallpaper changer.

Simple script to download top wallpaper from
/r/wallpaper and set it as desktop wallpaper
in LXDE & XFCE

for praw install use this:
pip3 install --user praw==3.6.2
"""
import os
import shlex
import shutil
import subprocess
from datetime import date, datetime
from pathlib import Path

import praw
import requests


def main():
    """Where the shit happens XD"""
    r = praw.Reddit(user_agent='Wallpaper Downloader')
    url = next(r.get_subreddit('earthporn').get_top_from_day(limit=1)).url
    req = requests.get(url, stream=True)
    directory = Path(os.getenv("HOME") + "/Pictures/Wallpapers/")
    if not directory.exists():
        directory.mkdir()
    current_time = date.isoformat(datetime.now())
    directory = directory / os.path.basename(current_time)
    with open(str(directory), 'wb') as f:
        shutil.copyfileobj(req.raw, f)
    output = subprocess.run(
        "ls /usr/bin/*session",
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True
        )
    if 'lxsession' in output.stdout:
        args = shlex.split(
            "pcmanfm -w --set-wallpaper={}".format(str(directory))
            )
    elif 'xfce4-session' in output.stdout:
        #check xfconf-query -c xfce4-desktop -p /backdrop -lv
        args = shlex.split(
            "xfconf-query -c xfce4-desktop -p " +
            "/backdrop/screen0/monitor0/workspace0/last-image  -s {}"
            .format(str(directory))
        )
    subprocess.Popen(args)


if __name__ == '__main__':
    main()
