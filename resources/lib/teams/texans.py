# coding=utf-8
import resources.lib.nflcs


class Team(resources.lib.nflcs.NFLCS):
    _short = "texans"
    _cdaweb_url = "http://www.houstontexans.com/cda-web/"
    _categories = [
        "Cheerleaders",
        "Community",
        # "Español",  # Does not return any videos, neither in Kodi or on the website
        "Football",
        "Friday Facebook Mailbag",
        "Gameday",
        "HCC",
        "NFL Network/NFL Films",
        "On The Road: Driven By Hyundai",
        "Press Conferences",
        "Season Highlights",
        "Special Segments",
        "Texans Huddle",
        "Texans TV",
        "TORO",
        "Training Camp presented by PC",
    ]

    def __init__(self, parameters):
        self._parameters = parameters
        self.go()
