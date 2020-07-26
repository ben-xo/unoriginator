#!/usr/bin/python3

import xml.sax
import re


class iTunesHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.depth = 0
        self.currentTag = ""
        self.inTrack = False
        self.nextStringIsName = False
        self.nextStringIsLocation = False
        self.trackName = ""
        self.trackLocation = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.depth += 1
        self.currentTag = tag
        if tag == 'dict' and self.depth == 4:
            self.inTrack = True

    # Call when an elements ends
    def endElement(self, tag):
        self.depth -= 1
        self.currentTag = ""
        if self.inTrack:
            if tag == 'dict':
                if re.match(r'^.*\(original mix\)$', self.trackName, flags=re.IGNORECASE):
                    print(self.trackLocation)
                self.trackName = ""
                self.trackLocation = ""
                self.inTrack = False
            elif tag == 'string':
                self.nextStringIsName = False
                self.nextStringIsLocation = False

    # Call when a character is read
    def characters(self, content):
        if self.inTrack:
            if self.currentTag == "key":
                if content == 'Name':
                    self.nextStringIsName = True
                elif content == 'Location':
                    self.nextStringIsLocation = True
            elif self.currentTag == 'string':
                if self.nextStringIsName:
                    self.trackName += content
                elif self.nextStringIsLocation:
                    self.trackLocation += content



if (__name__ == "__main__"):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = iTunesHandler()
    parser.setContentHandler(Handler)

    parser.parse("/Volumes/MUSIC/iTunes/iTunes Library.xml")