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

1. Make a Smart Playlist of "any of the following":
>     ends with `(original mix)`
>     ends with `(original)`
>     ends with `- original mix`
>     ends with `- original`

2. Select all the tracks

EITHER

3. Get Song Info
4. Change something minor, such as toggling the "Compilation of songs by different artists" flag

OR

3. Follow the guide [here](https://apple.stackexchange.com/questions/77193/is-there-a-way-to-force-itunes-11-to-update-tags/103445) to create a 'Refresh' menu option in iTunes (Mac only)

> Put the following into a file named `/Library/iTunes/Scripts/Refresh.scpt`
> ```
> tell application "iTunes"
>  repeat with aTrack in selection
>    try
>        refresh aTrack
>    end try
>  end repeat
> end tell
> ```



Credits
-------
Copyright 2020 Ben XO https://github.com/ben-xo/unoriginator
