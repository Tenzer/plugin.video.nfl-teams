import os
import sys
import time
from datetime import datetime

import xbmcaddon
import xbmcgui
import xbmcplugin


class Menu(object):
    _plugin_url = sys.argv[0]
    _handle = int(sys.argv[1])
    _addon_path = None

    def __init__(self, sort_methods=[]):
        addon = xbmcaddon.Addon(id="plugin.video.nfl-teams")
        self._addon_path = addon.getAddonInfo("path")

        for method in sort_methods:
            self._add_sort_method(method)

    def _add_sort_method(self, sort_method="none"):
        if sort_method == "none":
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_NONE)
        elif sort_method == "alpha":
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        elif sort_method == "date":
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_DATE)

    def add_item(self, url_params, name, folder=False, thumbnail=None, fanart=None, raw_metadata=None):
        params = ["?"]
        for key, value in url_params.iteritems():
            params.append("{0}={1}&".format(str(key), str(value)))
            if key is "team" and not fanart:
                fanart = os.path.join(self._addon_path, "resources", "images", "fanart", "{0}.jpg".format(value))

        url = "{0}{1}".format(self._plugin_url, "".join(params))

        if not thumbnail.startswith("http://"):
            thumbnail = os.path.join(self._addon_path, thumbnail)

        item = xbmcgui.ListItem()
        item.setLabel(name)

        if thumbnail:
            item.setThumbnailImage(thumbnail)
        if fanart:
            item.setProperty("fanart_image", fanart)

        info = {"title": name}

        if raw_metadata:
            info["plot"] = raw_metadata["description"]
            date = self.parse_video_date(raw_metadata["date"])
            if date:
                info["date"] = date.strftime("%d.%m.%Y")
                info["plot"] = "Added on {0}.\n{1}".format(date.strftime("%c"), info["plot"])

        item.setInfo("video", info)

        if folder:
            xbmcplugin.addDirectoryItem(self._handle, url, item, isFolder=folder)
        else:
            xbmcplugin.addDirectoryItem(self._handle, url, item)

    @classmethod
    def parse_video_date(cls, date_string):
        if date_string:
            try:
                return datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")
            except TypeError:
                return datetime.fromtimestamp(time.mktime(time.strptime(date_string, "%m/%d/%Y %H:%M:%S")))
        else:
            return None

    def end_directory(self):
        xbmcplugin.endOfDirectory(self._handle)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_directory()
        return False
