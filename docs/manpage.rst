Man Page
==============

.. important::
   This page uses auto-generation of ``--help`` option
   for different commands and script itself.

   Keep in mind that in commands usage
   there is no ``-f`` option of script itself.
   I call it "main option".

      For example, for 'display' command usage is:

      .. code:: none

         playlist-along display [OPTIONS]

      But in reality you must run as:

      .. code:: none

         playlist-along -f "path_to_playlist.m3u8" display [OPTIONS]

   In the future, there may be commands without the "main option".
   Or I'll try to correct ``--help`` output :)


.. click:: playlist_along.cli:cli_main
   :prog: playlist-along
   :nested: full