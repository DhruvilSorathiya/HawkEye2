# -------------------------------------------------------------------------------
# Name:         hep_myspace
# Purpose:      Query MySpace for username and location information.
#
# Author:      <bcoles@gmail.com>
#
# Created:     2018-10-07
# Copyright:   (c) bcoles 2018
# Licence:     MIT
# -------------------------------------------------------------------------------

import re

from hawkeye import HawkEyeEvent, HawkEyePlugin


class hep_myspace(HawkEyePlugin):

    meta = {
        'name': "MySpace",
        'summary': "Gather username and location from MySpace.com profiles.",
        'flags': [],
        'useCases': ["Footprint", "Investigate", "Passive"],
        'categories': ["Social Media"],
        'dataSource': {
            'website': "https://myspace.com/",
            'model': "FREE_NOAUTH_UNLIMITED",
            'references': [
                "https://www.programmableweb.com/api/myspace"
            ],
            'favIcon': "https://x.myspacecdn.com/new/common/images/favicons/favicon.ico",
            'logo': "https://x.myspacecdn.com/new/common/images/favicons/114-Retina-iPhone.png",
            'description': "Myspace is a place where people come to connect, discover, and share.\n"
            "Through an open design, compelling editorial features, "
            "and analytics-based recommendations, Myspace creates a creative community "
            "of people who connect around mutual affinity and inspiration for the purpose "
            "of shaping, sharing, and discovering what's next.",
        }
    }

    opts = {
    }

    optdescs = {
    }

    results = None

    def setup(self, hec, userOpts=dict()):
        self.he = hec
        self.__dataSource__ = "MySpace.com"
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    def watchedEvents(self):
        return ["EMAILADDR", "SOCIAL_MEDIA"]

    def producedEvents(self):
        return ["SOCIAL_MEDIA", "GEOINFO"]

    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.debug(f"Received event, {eventName}, from {srcModuleName}")

        # Search by email address
        if eventName == "EMAILADDR":
            email = eventData
            res = self.he.fetchUrl("https://myspace.com/search/people?q=" + email,
                                   timeout=self.opts['_fetchtimeout'],
                                   useragent=self.opts['_useragent'])

            if res['content'] is None:
                self.error(f"Could not fetch MySpace content for {email}")
                return

            # Extract HTML containing potential profile matches
            profiles = re.findall(r'<a href="/[a-zA-Z0-9_]+">[^<]+</a></h6>', str(res['content']))

            if not profiles:
                self.debug(f"No profiles found for e-mail: {email}")
                return

            # The first result is the closest match, but whether it's an exact match is unknown.
            profile = profiles[0]

            # Check for email address as name, at the risk of missed results.
            try:
                matches = re.findall(r'<a href=\"\/([a-zA-Z0-9_]+)\".*[\&; :\"\#\*\(\"\'\;\,\>\.\?\!]+' + email + r'[\&; :\"\#\*\)\"\'\;\,\<\.\?\!]+', profile, re.IGNORECASE)
            except Exception:
                self.debug("Malformed e-mail address, skipping.")
                return

            if not matches:
                self.debug("No concrete match for that e-mail.")
                return

            name = matches[0]
            e = HawkEyeEvent(
                "SOCIAL_MEDIA",
                f"MySpace: <HEURL>https://myspace.com/{name}</HEURL>",
                self.__name__,
                event
            )
            self.notifyListeners(e)

        # Retrieve location from MySpace profile
        if eventName == "SOCIAL_MEDIA":
            try:
                network = eventData.split(": ")[0]
                url = eventData.split(": ")[1].replace("<HEURL>", "").replace("</HEURL>", "")
            except Exception as e:
                self.debug(f"Unable to parse SOCIAL_MEDIA: {eventData} ({e})")
                return

            if network != "MySpace":
                self.debug(f"Skipping social network profile, {url}, as not a MySpace profile")
                return

            res = self.he.fetchUrl(url, timeout=self.opts['_fetchtimeout'],
                                   useragent=self.opts['_useragent'])

            if res['content'] is None:
                return

            data = re.findall(r'<div class="location_[^"]+" data-display-text="(.+?)"', res['content'])

            if not data:
                return

            location = data[0]

            if len(location) < 5 or len(location) > 100:
                self.debug("Skipping likely invalid location.")
                return

            e = HawkEyeEvent("GEOINFO", location, self.__name__, event)
            self.notifyListeners(e)

# End of hep_myspace class
