#!/usr/bin/python3

import xml.sax
import re
import urllib.parse
from pprint import pprint

import mutagen
from mutagen import MutagenError
from mutagen.id3 import ID3

ENDS_WITH_ORIGINAL_MIX = re.compile(r'^(.*?)\s*\(original mix\)$', re.I)

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
                if ENDS_WITH_ORIGINAL_MIX.match(self.trackName):
                    if self.trackLocation[0:8] == 'file:///':
                        filename = urllib.parse.unquote(self.trackLocation)[7:]
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
        print("** Checking %s" % filename)
        f = mutagen.File(filename)
        metadata_title = f.get('TIT2')

        if metadata_title is None:
            print(".. No TIT2 in file.")
            return

        print("++ Found %s" % metadata_title.text[0])
        m = ENDS_WITH_ORIGINAL_MIX.match(metadata_title.text[0])
        fixed_metadata_title = m[1]
        if metadata_title == fixed_metadata_title:
            print(".. Metadata title '%s' already looks fine to me." % metadata_title)
            return
        id3 = ID3(filename)
        print("++ ID3 version: {}".format(id3.version))
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