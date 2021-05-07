#!/usr/bin/env python3

"""

TW-S(napshot)notifier
    Copyright (C) 2021  Nicolas <stig124> FORMICHELLA

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; only using version 2 of the License

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


"""

"""
The RSS feed used is licensed under GPL2.0 to boombatower (https://github.com/boombatower/tumbleweed-review)
This only has utility in openSUSE Tumbleweed
"""


import os

import feedparser
import requests
from envparse import env
from plyer import notification


app_name = "tw_snotifier" # Change the app name here
icon1 = "/usr/share/pixmaps/distribution-logos/square-hicolor.svg" # Change icon here
path1 = "/usr/share/pixmaps/distribution-logos/" # And here

"""
Check for the tumbleweed logo in the default icon location
If not present, downloads it to user store (~/.icons or ~/.local/share/icons) from Commons
"""
if os.path.exists(path1) and os.path.isfile(icon1): # Be sure to check the variables otherwise the TW icon will be used
    app_icon = icon1
else:
    iname = "tw.svg"
    url = "https://upload.wikimedia.org/wikipedia/commons/4/49/OpenSUSE_Tumbleweed_green_logo.svg?download"
    with requests.get(url) as d:
        p1 = os.path.expanduser("~/.icons")
        p2 = os.path.expanduser("~/.local/share/icons")
        if os.path.exists(p1):
            path = p1
        elif os.path.exists(p2):
            path = p2
        else:
            os.mkdir(p1)
            path = p1
            with open(os.path.join(path, iname), "wb") as f:
                f.write(d.content)
                app_icon = os.path.join(path, iname)


def getsnapshot():
    """
    Get current running snapshot
    :return str version: str Version number
    """
    releasefile = "/usr/lib/os-release"
    env.read_envfile(releasefile)
    version = env.str('VERSION_ID').lower().rstrip()
    if len(version) == 0:
        raise EnvironmentError("Check /usr/lib/os-release")
    else:
        return str(version)


def rssparse(vid: str):
    """
    Parse RSS feed
    :param str vid: Actual running snapshot
    :return str returncode: 0 if no new version is found or the new version number
    """

    with requests.get("https://get.opensuse.org/api/v0/distributions.json") as r:
        if r.status_code == 200:
            feed = r.json()
            feed = feed['Tumbleweed'][0]['version']
        else:
            print("Falling back to RSS feed")
            dl = feedparser.parse('https://review.tumbleweed.boombatower.com/feed.xml')
            feed = str(dl.entries[0].title)
        returncode = rssprocess(feed, vid)
        return str(returncode)


def rssprocess(fed: str, version: str):
    """
    Process the latest RSS feed post title
    :param str fed: Title of the latest RSS feed post
    :param str version: Actual running snapshot
    :return: 0 if no new version and the actual version code if there is
    """
    s = fed.replace("Tumbleweed Release ", "").lower()
    if len(s) == 0:
        return 0
    else:
        if s > version:
            return s
        else:
            return 0


def title(rc: str, c: str):
    """
    Set the notification parameters
    :param str rc: Latest available snapshot or 0 if no updates
    :param str c: Actual running snapshot
    :return str: Notification parameters
    """
    if rc == "0":
        titler = "No Updates Available" # Notification title here (no updates available) and line 120 (updates available)
        timeoutr = 600 # Timeout (in seconds) here (no updates)
    else:
        titler = "Snapshot " + str(rc) + " available" + ", " + "running " + str(c)
        timeoutr = 3600 #Timeout (in seconds) here (updates available)

    return titler, timeoutr


def notif(array):
    """
    Sends notification
    :param array: Parameters arrays
    :return: Nothing
    """
    titled = str(array[0])
    timeoutd = int(array[1])
    notification.notify(title=titled, app_name=app_name, app_icon=app_icon, timeout=timeoutd,
                        toast=False)


if __name__ == '__main__':
    r_vid = getsnapshot()
    rrc = rssparse(r_vid)
    notifr = list(title(rrc, r_vid))
    notif(notifr)
