Contributor Guide
=================

Thank you for your interest in improving this project.
This project is open-source under the `MIT license`_ and
welcomes contributions in the form of
discussions, bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- `Source Code`_
- `Documentation`_
- `Discussions`_
- `Issue Tracker`_
- `Code of Conduct`_

.. _MIT license: https://opensource.org/licenses/MIT
.. _Source Code: https://github.com/hotenov/playlist-along
.. _Documentation: https://playlist-along.readthedocs.io/
.. _Discussions: https://github.com/hotenov/playlist-along/discussions
.. _Issue Tracker: https://github.com/hotenov/playlist-along/issues

How to report a bug
-------------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.
A playlist file (example) saved with your region encoding could help as well.


How to request a feature
------------------------

Request features on the `Discussions`_.


How to set up your development environment
------------------------------------------

You need Python 3.6.2+ and the following tools:

- Poetry_
- Nox_
- nox-poetry_

Install the package with development requirements:

.. code:: console

   $ poetry install

You can now run an interactive Python session,
or the command-line interface:

.. code:: console

   $ poetry run python
   $ poetry run playlist-along

.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/
.. _nox-poetry: https://nox-poetry.readthedocs.io/


How to test the project
-----------------------

Run the full test suite:

.. code:: console

   $ nox

.. attention::
   If you use PowerShell on Windows as your terminal,
   try to run each Nox command adding ``.exe``

   .. code-block:: bash

      nox.exe

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

.. code:: console

   $ nox --session=tests

Unit tests are located in the ``tests`` directory,
and are written using the pytest_ testing framework.

.. _pytest: https://pytest.readthedocs.io/


How to submit changes
---------------------

.. important::
   It is recommended to open an issue before starting work on anything.
   This will allow a chance to talk it over with the owners and validate your approach.

Fork the repository and clone it.

Create your local branch,
name it with issue number,
for example for issue #321:
``$ git checkout -b 321-short-clear-name``

Make changes in code, check linter and formatter warnings.

.. note::
   While we don't use 'pre-commit' as a Git hook,
   you should set up your IDE with linter and code formatter
   or use separate python packages for this.

   We prefer 'flake8' as Linter and 'black' as Formatter.

Commit your changes (do a series of small, atomic commits documenting your steps).

Push your local branch.

Open a `pull request`_ to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

.. _pull request: https://github.com/hotenov/playlist-along/pulls
.. github-only
.. _Code of Conduct: CODE_OF_CONDUCT.rst
