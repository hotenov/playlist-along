Usage Examples
==============

.. meta::
   :description: How to convert M3U playlist with square brackets for VLC for Android
   :keywords: playlist, M3U, VLC, Android, brackets, filename


.. important::
   All examples are written for Windows environment
   (because I mostly use the script on Windows 10),
   but all commands should work on Linux and Mac systems
   (with Unix paths, e.g. ``/home/user/Downloads/``).
   Python 3.6.2+ is all what you need on any OS.
   And don't afraid Russian songs and Cyrillic paths in examples.



For current version, it's assumed that you have playlist saved in "AIMP format"
(i.e. M3U tags and file paths are on separate lines),
for example:

.. code-block:: python

   #EXTM3U
   #EXTINF:238,MONATIK, Вера Брежнева - ВЕЧЕРиНОЧКА
   D:\tmp\tmp_mp3\cp1251\01 MONATIK, Вера Брежнева - ВЕЧЕРиНОЧКА [rus pop dance].mp3
   #EXTINF:267,Dabro - Юность (Mikis Remix)
   D:\tmp\tmp_mp3\cp1251\02 Dabro - Юность (Mikis Remix) [rus dance].mp3

or simple playlist file with tracks on each line:

.. code-block:: python

   D:\tmp\tmp_mp3\cp1251\01 MONATIK, Вера Брежнева - ВЕЧЕРиНОЧКА [rus pop dance].mp3
   D:\tmp\tmp_mp3\cp1251\02 Dabro - Юность (Mikis Remix) [rus dance].mp3
   D:\tmp\tmp_mp3\cp1251\03 IOWA - Потанцуй Со Мной (JONVS Radio Remix) [rus pop dance].mp3

Basic
----------

Displaying tracklist
~~~~~~~~~~~~~~~~~~~~

You can display (print) in terminal only tracks from your playlist:

.. code-block:: bash

   playlist-along --file "D:\tmp\tmp_m3u\AIMP-example.m3u8" display

or shorter, with the same result:

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8"

Convert M3U for VLC for Android
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

For copying songs from origin playlist to folder with converted playlist, use option ``--copy``

.. code-block:: bash

   playlist-along -f "D:\tmp\tmp_m3u\AIMP-example.m3u8" convert -d "D:\tmp\tmp_m3u\new destination" --copy

.. important::
   Currently script DOES NOT override existing audio files in destination folder.
   There is a restriction for audio formats as well (only ``.mp3``, ``.flac``).


Advanced
----------

Folder with . (dot)
~~~~~~~~~~~~~~~~~~~

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