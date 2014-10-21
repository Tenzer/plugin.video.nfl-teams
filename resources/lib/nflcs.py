import urllib
import urllib2
from json import load

import xbmc
import xbmcaddon
import xbmcgui
from resources.lib.menu import Menu


class NFLCS(object):
    _short = str(None)
    _fanart = str(None)
    _cdaweb_url = str(None)
    _categories = list()
    _categories_strip_left = [
        "Pandora ",
        "Video - ",
        "Videos - ",
    ]
    _parameters = list()

    def go(self):
        if "id" in self._parameters:
            self.play_video()
        elif "category" in self._parameters:
            self.list_videos()
        else:
            self.list_categories()

    def play_video(self):
        get_parameters = {"id": self._parameters["id"][0]}
        data = urllib.urlencode(get_parameters)
        request = urllib2.Request("{0}audio-video-content.htm".format(self._cdaweb_url), data)
        response = urllib2.urlopen(request)
        json = load(response, "iso-8859-1")
        title = json["headline"]
        thumbnail = json["imagePaths"]["xl"]

        remotehost = json["cdnData"]["streamingRemoteHost"]
        if "a.video.nfl.com" in remotehost:
            remotehost = remotehost.replace("a.video.nfl.com", "vod.hstream.video.nfl.com")

        max_bitrate = int(xbmcaddon.Addon("plugin.video.nfl-teams").getSetting("max_bitrate")) * 1000000 or 5000000
        bitrate = -1
        lowest_bitrate = None
        for path_entry in json["cdnData"]["bitrateInfo"]:
            if path_entry["rate"] > bitrate and path_entry["rate"] <= max_bitrate:
                path = path_entry["path"]
                bitrate = path_entry["rate"]
            if not lowest_bitrate or path_entry["rate"] < lowest_bitrate:
                lowest_path = path_entry["path"]
                lowest_bitrate = path_entry["rate"]

        if not path:
            path = lowest_path

        if not path.startswith("http://"):
            path = "{0}{1}?r=&fp=&v=&g=".format(remotehost, path)

        listitem = xbmcgui.ListItem(title, thumbnailImage=thumbnail)
        listitem.setProperty("PlayPath", path)
        xbmc.Player().play(path, listitem)

    def list_videos(self):
        if self._parameters["category"][0] == "all":
            parameters = {"type": "VIDEO", "channelKey": ""}
        else:
            parameters = {"type": "VIDEO", "channelKey": self._parameters["category"][0]}

        data = urllib.urlencode(parameters)
        request = urllib2.Request("{0}audio-video-channel.htm".format(self._cdaweb_url), data)
        response = urllib2.urlopen(request)
        json = load(response, "iso-8859-1")

        with Menu(["date", "alpha"]) as menu:
            for video in json["gallery"]["clips"]:
                menu.add_item({
                    "url_params": {"team": self._short, "id": video["id"]},
                    "name": video["title"],
                    "folder": False,
                    "thumbnail": video["thumb"],
                    "raw_metadata": video
                })

    def list_categories(self):
        with Menu(["none"]) as menu:
            menu.add_item({
                "url_params": {"team": self._short, "category": "all"},
                "name": "All Videos",
                "folder": True,
                "thumbnail": "resources/images/{0}.png".format(self._short)
            })
            for category in self._categories:
                raw_category = category

                for strip_left in self._categories_strip_left:
                    if category.startswith(strip_left):
                        category = category[(len(strip_left)):]

                menu.add_item({
                    "url_params": {"team": self._short, "category": raw_category},
                    "name": category,
                    "folder": True,
                    "thumbnail": "resources/images/{0}.png".format(self._short)
                })
