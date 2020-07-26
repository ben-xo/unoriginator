#!/usr/bin/env python3

import xml.sax
import re
import urllib.parse
import os
import sys
import mutagen
from mutagen import MutagenError
from mutagen.id3 import ID3, TIT2

ENDS_WITH_ORIGINAL_MIX = re.compile(r'^(.*?)\s*\(original mix\)$', re.I)

total_seen_files = 0
total_updated_files = 0
total_itunes_entries = 0
didnt_process = []

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
        global total_itunes_entries
        self.depth -= 1
        self.currentTag = ""
        if self.inTrack:
            if tag == 'dict':
                if ENDS_WITH_ORIGINAL_MIX.match(self.trackName):
                    if self.trackLocation[0:8] == 'file:///':
                        filename = urllib.parse.unquote(self.trackLocation)[7:]
                        update_tag(filename)
                self.trackName = ""
                self.trackLocation = ""
                self.inTrack = False
                total_itunes_entries += 1
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


def update_tag(filename):
    global total_updated_files
    global total_seen_files
    global didnt_process

    total_seen_files += 1
    try:
        print("** Checking %s" % filename)

        # id3 = ID3(filename)
        # print("++ ID3 version: {}".format(id3.version))

        f = mutagen.File(filename)
        metadata_title = f.get('TIT2')

        if metadata_title is None:
            print(".. No TIT2 in file.")
            didnt_process.append(filename)
            return

        print("++ Found %s" % metadata_title.text[0])
        m = ENDS_WITH_ORIGINAL_MIX.match(metadata_title.text[0])
        if m is not None:
            fixed_metadata_title = m[1]
            if metadata_title == fixed_metadata_title:
                print(".. Metadata title '%s' already looks fine to me." % metadata_title)
                return

            f.tags.add(TIT2(text=[fixed_metadata_title]))
            f.save()
            total_updated_files += 1
            return
        else:
            print(".. Did mot match (original mix) for {}".format(filename))

    except MutagenError as e:
        print("!! Could not read file: {}".format(e))
    except AttributeError:
        print('!! No tags found: {}'.format(e))

    didnt_process.append(filename)


if __name__ == "__main__":
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = iTunesHandler()
    parser.setContentHandler(Handler)

    if sys.argv[1] is None:
        path = os.path.join(os.getenv("HOME"), "Music/iTunes/iTunes Library.xml")
    else:
        path = sys.argv[1]

    parser.parse(path)

    print()
    print("Total iTunes entries parsed:  {}".format(total_itunes_entries))
    print("Total candidate files to fix: {}".format(total_seen_files))
    print("Total files actually fixed:   {}".format(total_updated_files))
    if len(didnt_process) > 0:
        print("Didn't process the following files:")
        for i in didnt_process:
            print("\t{}".format(i))