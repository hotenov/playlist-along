Playlist Along
==============

|Status| |PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|
|Black|

.. |Status| image:: https://raster.shields.io/badge/Status-alpha-orange
   :target: https://raster.shields.io/badge/Status-alpha-orange
   :alt: Project Status
.. |PyPI| image:: https://img.shields.io/pypi/v/playlist-along.svg
   :target: https://pypi.org/project/playlist-along/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/playlist-along
   :target: https://pypi.org/project/playlist-along
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/playlist-along.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/playlist-along/latest.svg?label=Read%20the%20Docs
   :target: https://playlist-along.readthedocs.io/
   :alt: Read the documentation at https://playlist-along.readthedocs.io/
.. |Tests| image:: https://github.com/hotenov/playlist-along/workflows/Tests/badge.svg
   :target: https://github.com/hotenov/playlist-along/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/hotenov/playlist-along/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/hotenov/playlist-along
   :alt: Codecov
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

🧐 About
---------

Have you ever wanted to take your favorite offline playlist along?
— *I have.*

This script makes it easier to do that.
It converts your playlist with absolute paths
to playlist with relative paths,
and copies audio files to one folder with converted playlist.
The only thing that remains to be done is to move this folder
to your Android smartphone and open the playlist
(or let a player to discover media for you).

Although, there is only one conversion way
"Desktop `AIMP`_ -> `VLC for Android`_" for now, 
but who knows what the future holds for us?

🚀 Features
------------

*  Conversion from **AIMP** *(desktop)* .m3u / .m3u8 playlists
   into playlists suitable for playback in **VLC for Android**
   (with relative paths,
   replaced square brackets ``[`` ``]`` and *hash* ``#`` 
   in songs filenames)
*  Copying songs from .m3u / .m3u8 playlists into destination folder
   (after playlist conversion and only **.mp3** and **.flac** local files, for now)
*  Displaying only tracks from playlist
   *(without M3U tag lines / comments)*
*  **TBD:** Displaying a full content of playlist file
*  **TBD:** Creating a playlist from tracks in specified folder
   (with relative or absolute paths)
*  **TBD:** Injecting (appending) one playlist into another 
   (top or bottom)
*  **TBD:** Creating an empty playlist file
*  **TBD:** Copying and conversion paths to relative, without replacing characters
   ("make relative playlist")

🛠️ Requirements
----------------

* Python 3.6.2 and higher


💻 Installation
----------------

You can install *Playlist Along* via pip_ from PyPI_:

.. code:: console

   $ pip install playlist-along

I do recommend you to use `pipx`_ for any CLI Python package.
It let you install and run Python applications in isolated environments.

.. code:: console

   $ python -m pip install --user pipx
   $ pipx install playlist-along
   $ playlist-along --version

🕹 Usage
--------

Please see the `Usage Examples <Usage_>`_ or the `Command-line Reference <Manpage_>`_ for details.


✊ Contributing
---------------

If you want to suggest a new feature or to ask questions about this project,
you can open a `new discussion`_.

Want to implement or fix something? - contributions are very welcome.
To learn more, see the `Contributor Guide`_.


📝 License
-----------

Distributed under the terms of the `MIT license`_,
*Playlist Along* is free and open source software.


🐞 Issues
----------

If you encounter any problems,
please see `project discussions`_ first 
or `file an issue`_ along with a detailed description.


🙏🏻 Credits
------------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

We use the following packages / libraries under the hood:

* `Click`_, of course (`BSD-3-Clause License <https://github.com/pallets/click/blob/main/LICENSE.rst>`_)
* `charset_normalizer <https://github.com/Ousret/charset_normalizer>`_, for auto encoding detecting of playlist files (MIT License)
* `single-source <https://github.com/rabbit72/single-source>`_, for getting project version from anywhere (MIT License)


.. _AIMP: https://www.aimp.ru/
.. _VLC for Android: https://play.google.com/store/apps/details?id=org.videolan.vlc&hl=en&gl=US
.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/project/playlist-along/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/hotenov/playlist-along/issues
.. _pip: https://pip.pypa.io/
.. _new discussion: https://github.com/hotenov/playlist-along/discussions/new
.. _project discussions: https://github.com/hotenov/playlist-along/discussions
.. _Click: https://github.com/pallets/click
.. _pipx: https://pipxproject.github.io/pipx/

.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://playlist-along.readthedocs.io/en/latest/usage.html
.. _Manpage: https://playlist-along.readthedocs.io/en/latest/manpage.html
