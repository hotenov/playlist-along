Usage Examples
==============

.. meta::
   :description: How to convert M3U playlist with square brackets for VLC for Android
   :keywords: playlist, M3U, VLC, Android, brackets, filename


.. important::
   All examples are written for the Windows environment
   (because I mostly use the script on Windows 10),
   but all commands should work on the Linux and Mac OS platforms
   (with Unix paths, e.g. ``/home/user/Downloads/``).
   In fact, Python 3.6.2+ is all what you need on any OS.


For current version, it's assumed that you have `Extended M3U`_ file
(i.e. M3U tags and file paths are on **separate** lines),
for example:

.. _Extended M3U: https://en.wikipedia.org/wiki/M3U#Extended_M3U

.. code:: none

   #EXTM3U
   #EXTINF:123, Sample artist - Sample title
   C:\Documents and Settings\I\My Music\Sample with [brackets].mp3
   #EXTINF:321,Example Artist - Example title
   C:\Documents and Settings\I\My Music\Greatest Hits\Example #02.mp3

or simple playlist file with tracks on each line:

.. code:: none

   Stuff.mp3
   D:\More Music\Foo.mp3

Basic
----------

How to display tracklist
~~~~~~~~~~~~~~~~~~~~~~~~~

You can display (print) in a terminal only tracks from your playlist:

.. code-block:: bash

   playlist-along --file "D:\tmp\tmp_m3u\AIMP-example.m3u8" display

or shorter, with the same result:

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8"

How to convert M3U for VLC for Android
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To convert only playlist (without copying files), use this command:

.. code-block:: bash

   playlist-along --file "D:\tmp\tmp_m3u\AIMP-example.m3u8" convert --dest "D:\tmp\tmp_m3u\new destination"

or with short options:

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8" convert -d "D:\tmp\tmp_m3u\new destination"

If you want to rename converted playlist or save into another format,
specify a full path for destination:

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8" convert -d "D:\tmp\tmp_m3u\new destination\my-phone.m3u"

.. hint::
   All intermediate sub-directories for destination will be created automatically. 
   You don't have to worry about it.

.. note::
   If you specify the same path as origin playlist for new destination, 
   script will NOT override your origin playlist.
   Instead of this, it append suffix ``_vlc`` for converted playlist name.

How to convert playlist and copy its audio files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For copying songs from origin playlist to folder with converted playlist, use option ``--copy``

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8" convert -d "D:\tmp\tmp_m3u\new destination" --copy

.. important::
   Currently script DOES NOT override existing audio files in destination folder.
   There is a restriction for audio formats as well (only ``.mp3``, ``.flac``).


How to create M3U with tracks in a folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create (generate) a playlist with absolute paths to audio files
in certain folder and place this playlist somewhere,
you can use this command:

.. code-block:: bash

   playlist-along -f "D:\tmp\pls\new.m3u8" create --from "D:\tmp\tmp_mp3" --abs

If you want create a playlist with relative paths
and place it along with audio tracks (in the same folder),
you should use ``--here`` option.
In that case a full path to playlist can be omitted.
You need only its name and format.
Relative paths are by default:

.. code-block:: bash

   playlist-along -f "name.m3u8" create -f "D:\tmp\tmp_mp3" --here

Do you like extended M3U? No problem.
Use option ``--ext-m3u``:

.. code-block:: bash

   playlist-along -f "name.m3u8" create -f "D:\tmp\tmp_mp3" --here --ext-m3u

Windows users could get used to 'natural sort order' in their Explorer windows.
You can apply exact the same order for playlist as you see files in Windows Explorer:

.. code-block:: bash

   playlist-along -f "D:\tmp\pls\new.m3u8" create --from "D:\tmp\tmp_mp3" --abs --nat-sort

Or maybe in reversed order? ``-REV`` will help you:

.. code-block:: bash

   playlist-along -f "D:\tmp\pls\new.m3u8" create --from "D:\tmp\tmp_mp3" --abs --nat-sort -REV

.. important::
   Script creates all playlist files only in ``UTF-8`` encoding. 
   Is that a problem for you - let me know.

Advanced
----------

How to use folder with . (dot)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For saving converted playlist and copying files
into a folder, containing ``.`` (dot) in its name,
you should tell script about your intention.
Use option ``--dir`` for **convert** command:

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8" convert -d "D:\tmp\tmp_m3u\pls.m3u" --dir --copy

.. attention::
   Now, you **cannot rename** a converted playlist in this case.
   If you really want this feature, let me know
   in `discussions <https://github.com/hotenov/playlist-along/discussions>`_

How to create an empty playlist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For some reason you might need to create an empty playlist
and then add tracks into it manually in player.
Option ``--empty`` is just for this purpose:

.. code-block:: bash

   playlist-along -f "D:\tmp\pls\blank.m3u8" create --empty