Why?
====

My short (True) story
---------------------

I often use square brackets ``[`` ``]`` in my mp3 filenames.
I've started to organize my offline music collection with .m3u8 playlists,
saved via AIMP (my favorite audio player on Windows PC).
However, I use 'VLC for Android' as universal player
(all in one place) on my smartphone.

Soon, I ran into problem with square brackets in filenames inside M3U playlists in VLC for Android.
On google, I found out that this is normal behavior for VLC, and developers `won't fix this`_
**(UPD: at least until 2023)**.
Although, many people are suffering (me too). See linked issues and many posts on the Internet.

"OK, No problem!" - I thought. "I will replace brackets using percent-encoding."
(also known as URL encoding), i.e. ``%5B`` and ``%5D`` respectively.
Later I found out that ``#`` sigh also needs to be replaced with ``%23``.

So this project (script) appeared.

.. _won't fix this: https://code.videolan.org/videolan/vlc/-/issues/19567

Initial Logic
--------------

*  It takes and read original playlist file with absolute paths.
*  Then It cuts absolute (full) file path, leaving only file name
   (tail or the `final path component`_ in 'pathlib')
*  Then it replaces (substitutes) ``[`` ``]`` ``#`` with ``%5B`` and ``%5D`` and ``%23``
*  Finally, it saves converted playlist file (with relative paths) by specified destination.

.. _final path component: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name

Possible Roadmap
-----------------

As my personal project,
I'd like to automate my other routine tasks related to playlists.
That's why I'll try to implement the following features:

*  Displaying a full content of playlist file
*  Creating a playlist from tracks in specified folder
   (with relative or absolute paths)
*  Injecting (appending) one playlist into another 
   (top or bottom)
*  Creating an empty playlist file (using current date, for example)
*  Copying and conversion paths to relative, without replacing characters
   ("make relative playlist")
*  Creating CUE sheet file from text file with timing
   (similar to online `CUEgenerator`_, which I use manually now)

.. _CUEgenerator: https://cuegenerator.net/

