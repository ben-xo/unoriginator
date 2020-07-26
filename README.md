The Unoriginator
================

Bulk remove those pesky "(Original Mix)" suffixes from every track in your iTunes library, so that they scrobble better to Last.fm

Usage
-----

1. python3 -mvenv unoriginator
2. . ./unoriginator/bin/activate
3. pip install mutagen
4. ./unoriginator.py

How to get iTunes to see the changes
------------------------------------

1. Make a Smart Playlist of "ends with (original mix)"
2. Select all the tracks
3. Get Song Info
4. Change something minor, such as toggling the "Compilation of songs by different artists" flag

Credits
-------
Copyright 2020 Ben XO https://github.com/ben-xo/unoriginator
