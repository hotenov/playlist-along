Why?
====

My Short (True) Story
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
Later I found out that ``#`` sign also needs to be replaced with ``%23``.

So this project (script) appeared.

.. _won't fix this: https://code.videolan.org/videolan/vlc/-/issues/19567

Initial Logic
--------------

*  It takes and read origin playlist file with absolute paths.
*  Then It cuts absolute (full) file path, leaving only file name
   (tail or the `final path component`_ in 'pathlib')
*  Then it replaces (substitutes) ``[`` ``]`` ``#`` with ``%5B`` and ``%5D`` and ``%23``
*  Finally, it saves converted playlist file (with relative paths) by specified destination.

Take a look:

.. tab:: ORIGIN

   .. code:: none

      #EXTM3U
      #EXTINF:123, Sample artist - Sample title
      C:\Documents and Settings\I\My Music\Sample with [brackets].mp3
      #EXTINF:321,Example Artist - Example title
      C:\Documents and Settings\I\My Music\Greatest Hits\Example #02.mp3

.. tab:: CONVERTED

   .. code:: none

      #EXTM3U
      #EXTINF:123, Sample artist - Sample title
      Sample with %5Bbrackets%5D.mp3
      #EXTINF:321,Example Artist - Example title
      Example %2302.mp3


.. _final path component: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name

Possible Roadmap
-----------------

As my personal project,
I'd like to automate my other routine tasks related to playlists.
That's why I'll try to implement the following features:

*  Displaying a full content of playlist file `(ready in v2021.6.1)`
*  Creating a playlist from tracks in specified folder 
   (with relative or absolute paths) `(ready in v2021.6.1)`
*  Injecting (appending) one playlist into another 
   (top or bottom) `(ready in v2021.6.1)`
*  Creating an empty playlist file
   `(ready in v2021.6.1)`
*  Copying and conversion paths to relative, without replacing characters
   ("make relative playlist")
*  Creating CUE sheet file from text file with timing
   (similar to online `CUEgenerator`_, which I use manually now)

.. _CUEgenerator: https://cuegenerator.net/

