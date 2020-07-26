#!/usr/bin/python3

import xml.sax
import re
import urllib.parse

from mutagen import MutagenError
from mutagen.aiff import AIFF
from mutagen.mp3 import MP3
from mutagen.wave import WAVE


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
                if re.match(r'^.*\(original mix\)$', self.trackName, flags=re.I):
                    if self.trackLocation[0:8] == 'file:///':
                        filename = urllib.parse.unquote(self.trackLocation)[7:]
                        print ("** %s" % filename)
                        updateTag(filename)
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


def updateTag(filename):
    try:
        if re.match(r'^.*\.mp3', filename, re.I):
            mp3 = MP3(filename)
            print(mp3.tags.getall('TIT2'))
        elif re.match(r'^.*\.aiff?', filename, re.I):
            aiff = AIFF(filename)
            print(aiff.tags.getall('TIT2'))
        elif re.match(r'^.*\.wav', filename, re.I):
            wav = WAVE(filename)
            print(wav.tags.getall('TIT2'))
        else:
            print("!! Unsure what format %s is" % filename)
    except MutagenError:
        print("!! Could not read file")
    except AttributeError:
        print('!! No tags found')


if (__name__ == "__main__"):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = iTunesHandler()
    parser.setContentHandler(Handler)

    parser.parse("/Volumes/MUSIC/iTunes/iTunes Library.xml")