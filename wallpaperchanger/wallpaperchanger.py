"""wallpaperchanger.py - simple wallpaper changer.

Simple script to download top wallpaper from
/r/wallpaper and set it as desktop wallpaper
in LXDE
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
    url = next(r.get_subreddit('wallpaper').get_top_from_day(limit=1)).url
    req = requests.get(url, stream=True)
    dir = Path(os.getenv("HOME") + "/wallpapers/")
    if not dir.exists():
        dir.mkdir()
    current_time = date.isoformat(datetime.now())
    dir = dir / os.path.basename(current_time)
    with open(str(dir), 'wb') as f:
        shutil.copyfileobj(req.raw, f)
    args = shlex.split(
        "pcmanfm -w --set-wallpaper={}".format(str(dir))
        )
    subprocess.Popen(args)


if __name__ == '__main__':
    main()
