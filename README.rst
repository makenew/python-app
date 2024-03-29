Python App Skeleton
===================

|PyPI| |GitHub Actions|

.. |PyPI| image:: https://img.shields.io/pypi/v/makenew-python-app.svg
   :target: https://pypi.python.org/pypi/makenew-python-app
   :alt: PyPI
.. |GitHub Actions| image:: https://github.com/makenew/python-app/workflows/main/badge.svg
   :target: https://github.com/makenew/python-app/actions
   :alt: GitHub Actions

Package skeleton for a Python app.

Description
-----------

Bootstrap a new Python_ app in less than a minute.

.. _Python: https://www.python.org/

Features
~~~~~~~~

- Publishing to PyPI_.
- Secure dependency management with Poetry_.
- Multi-stage Docker_ builds for optimized production images.
- Images tagged using package version and commit checksum.
- Images pushed to `GitHub Container Registry`_.
- Standardized JSON logging with structlog_.
- Centralized dependency injection with pinject_.
- Tornado_ with asyncio.
- Linting with Pylint_.
- Uncompromising code formatting with Black_.
- pytest_ helps you write better programs.
- Code coverage reporting with Codecov_.
- Continuous unit and smoke testing and deployment with `GitHub Actions`_.
- `Keep a CHANGELOG`_.
- Consistent coding with EditorConfig_.
- Badges from Shields.io_.

.. _Black: https://black.readthedocs.io/en/stable/
.. _Codecov: https://codecov.io/
.. _Docker: https://www.docker.com/
.. _EditorConfig: https://editorconfig.org/
.. _GitHub Actions: https://github.com/features/actions
.. _GitHub Container Registry: https://github.com/features/packages
.. _Keep a CHANGELOG: https://keepachangelog.com/
.. _PyPI: https://pypi.python.org/pypi
.. _Pylint: https://www.pylint.org/
.. _Shields.io: https://shields.io/
.. _Tornado: https://www.tornadoweb.org/
.. _pinject: https://pypi.org/project/pinject/
.. _pytest: https://docs.pytest.org/
.. _structlog: http://www.structlog.org/

Bootstrapping a New Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create an empty (**non-initialized**) repository on GitHub.
2. Clone the master branch of this repository with

   ::

       $ git clone --single-branch https://github.com/makenew/python-app.git new-python-app
       $ cd new-python-app

   Optionally, reset to the latest
   `release <https://github.com/makenew/python-app/releases>`__ with

   ::

       $ git reset --hard <version-tag>

3. Run

   ::

       $ ./makenew.sh

   This will replace the boilerplate, delete itself,
   remove the git remote, remove upstream tags,
   and stage changes for commit.

4. Create the required GitHub repository secrets
5. Review, commit, and push the changes to GitHub with

   ::

     $ git diff --cached
     $ git commit -m "Replace makenew boilerplate"
     $ git remote add origin git@github.com:<user>/<new-python-app>.git
     $ git push -u origin master

6. Ensure the GitHub action passes,
   then publish the initial version of the package with

   ::

     $ poetry install
     $ poetry version patch
     $ make version

Updating
~~~~~~~~

If you want to pull in future updates from this skeleton,
you can fetch and merge in changes from this repository.

Add this as a new remote with

::

    $ git remote rename origin upstream

and then configure your ``origin`` branch as normal.

Otherwise, add this as a new remote with

::

    $ git remote add upstream git@github.com:makenew/python-app.git

You can then fetch and merge changes with

::

    $ git fetch --no-tags upstream
    $ git merge upstream/master

Changelog
^^^^^^^^^

Note that ``CHANGELOG.md`` is just a template for this skeleton. The
actual changes for this project are documented in the commit history and
summarized under
`Releases <https://github.com/makenew/python-app/releases>`__.

Usage
-----

Docker container
~~~~~~~~~~~~~~~~

The service is distributed as a Docker container on GitHub Container Registry.
To run locally, add configuration to `config/local.json`,
then pull and run the image with

::

    $ docker run --read-only --init --publish 8080:8080 \
      --volume "$(pwd)/config/local.json:/usr/src/app/config/local.json" \
      ghcr.io/makenew/python-app

Installation
------------

This package is also registered on the `Python Package Index (PyPI)`_
as makenew-python-app_.

Install it with

::

    $ poetry add makenew-python-app

.. _makenew-python-app: https://pypi.python.org/pypi/makenew-python-app
.. _Python Package Index (PyPI): https://pypi.python.org/

Development and Testing
-----------------------

Quickstart
~~~~~~~~~~

::

    $ git clone https://github.com/makenew/python-app.git
    $ cd python-app
    $ poetry install

Run each command below in a separate terminal window:

::

    $ make watch
    $ make server

Primary development tasks are defined in the `Makefile`.

Source Code
~~~~~~~~~~~

The `source code`_ is hosted on GitHub.
Clone the project with

::

    $ git clone https://github.com/makenew/python-app.git

.. _source code: https://github.com/makenew/python-app

Requirements
~~~~~~~~~~~~

You will need `Python 3`_ and Poetry_.

Install the development dependencies with

::

    $ poetry install

.. _Poetry: https://poetry.eustace.io/
.. _Python 3: https://www.python.org/

Tests
~~~~~

Lint code with

::

    $ make lint


Run tests with

::

    $ make test

Run tests on changes with

::

    $ make watch

Publishing
~~~~~~~~~~

Use the `poetry version`_ command to release a new version.
Then run `make version` to commit and push a new git tag
which will trigger a GitHub action.

Publishing may be triggered using a `version workflow_dispatch on GitHub Actions`_.

.. _Poetry version: https://python-poetry.org/docs/cli/#version
.. _version workflow_dispatch on GitHub Actions: https://github.com/makenew/pypackage/actions?query=workflow%3Aversion

GitHub Actions
--------------

*GitHub Actions should already be configured: this section is for reference only.*

The following repository secrets must be set on GitHub Actions.

- ``PYPI_API_TOKEN``: API token for publishing on PyPI.
- ``GH_USER``: The GitHub user's username to pull and push containers.
- ``GH_TOKEN``: A personal access token for the user.

These must be set manually.

Secrets for Optional GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The version and format GitHub actions
require a user with write access to the repository
including access to read and write packages.
Set these additional secrets to enable the action:

- ``GH_TOKEN``: A personal access token for the user.
- ``GIT_USER_NAME``: The name to set for Git commits.
- ``GIT_USER_EMAIL``: The email to set for Git commits.
- ``GPG_PRIVATE_KEY``: The `GPG private key`_.
- ``GPG_PASSPHRASE``: The GPG key passphrase.

.. _GPG private key: https://github.com/marketplace/actions/import-gpg#prerequisites

Contributing
------------

Please submit and comment on bug reports and feature requests.

To submit a patch:

1. Fork it (https://github.com/makenew/python-app/fork).
2. Create your feature branch (`git checkout -b my-new-feature`).
3. Make changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin my-new-feature`).
6. Create a new Pull Request.

License
-------

This Python app is licensed under the MIT license.

Warranty
--------

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall the copyright holder or contributors be liable for
any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services;
loss of use, data, or profits; or business interruption) however caused and on
any theory of liability, whether in contract, strict liability, or tort
(including negligence or otherwise) arising in any way out of the use of this
software, even if advised of the possibility of such damage.
