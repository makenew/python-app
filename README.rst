Python App Skeleton
===================

|PyPI| |Docker| |Codecov| |CircleCI|

.. |PyPI| image:: https://img.shields.io/pypi/v/makenew-python-app.svg
   :target: https://pypi.python.org/pypi/makenew-python-app
   :alt: PyPI
.. |Docker| image:: https://img.shields.io/docker/pulls/makenew/python-app.svg
   :target: https://hub.docker.com/r/makenew/python-app
   :alt: Docker
.. |Codecov| image:: https://img.shields.io/codecov/c/github/makenew/python-app.svg
   :target: https://codecov.io/gh/makenew/python-app
   :alt: Codecov
.. |CircleCI| image:: https://img.shields.io/circleci/project/github/makenew/python-app.svg
   :target: https://circleci.com/gh/makenew/python-app
   :alt: CircleCI

Package skeleton for an Python app.

Description
-----------

Bootstrap a new Python_ app in less than a minute.

.. _Python: https://www.python.org/

Features
~~~~~~~~

- Publishing to PyPI_.
- Secure dependency management with Poetry_.
- `Alpine Linux`_ based multi-stage Docker_ builds for optimized production images.
- Images tagged using package version and commit checksum.
- Images pushed to `Docker Hub`_, Heroku_, Bintray_ and the `Amazon EC2 Container Registry (ECR)`_.
- Standardized JSON logging with structlog_.
- Centralized dependency injection with pinject_.
- Tornado_ with asyncio.
- Linting with Pylint_.
- pytest_ helps you write better programs.
- Code coverage reporting with Codecov_.
- Continuous unit and smoke testing and deployment with CircleCI_.
- `Keep a CHANGELOG`_.
- Consistent coding with EditorConfig_.
- Badges from Shields.io_.

.. _Alpine Linux: https://alpinelinux.org/
.. _Amazon EC2 Container Registry (ECR): https://aws.amazon.com/ecr/
.. _Bintray: https://bintray.com/
.. _Codecov: https://codecov.io/
.. _Docker Hub: https://hub.docker.com/
.. _Docker: https://www.docker.com/
.. _EditorConfig: https://editorconfig.org/
.. _Heroku: https://www.heroku.com/
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

       $ git reset --hard v1.2.0

3. Run

   ::

       $ ./makenew.sh

   This will replace the boilerplate, delete itself,
   remove the git remote, remove upstream tags,
   and stage changes for commit.

4. Create the required CircleCI environment variables with

   ::

       $ .circleci/envvars.sh

5. Review, commit, and push the changes to GitHub with

   ::

     $ git diff --cached
     $ git commit -m "Replace makenew boilerplate"
     $ git remote add origin git@github.com:<user>/<new-python-app>.git
     $ git push -u origin master

6. Ensure the CircleCI build passes,
   then publish the initial version of the package with

   ::

     $ poetry install
     $ poetry run bumpversion patch
     $ git push
     $ git push --tags

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

The service is distributed as a Docker container on Docker Hub.
To run locally, add configuration to `config/local.json`,
then pull and run the image with

::

    $ docker run --read-only --init --publish 8080:8080 \
      --volume "$(pwd)/config/local.json:/usr/src/app/config/local.json" \
      makenew/python-app

Installation
------------

This package is also registered on the `Python Package Index (PyPI)`_
as makenew_python_app_.

Install it with

::

    $ poetry install makenew_python_app

.. _makenew_python_app: https://pypi.python.org/pypi/makenew-python-app
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

Run tests on chages with

::

    $ make watch

Publishing
~~~~~~~~~~

Use the bumpversion_ command to release a new version.
Push the created git tag which will trigger a CircleCI publish job.

.. _bumpversion: https://github.com/peritus/bumpversion

CircleCI Setup
--------------

*CircleCI should already be configured: this section is for reference only.*

The following environment variables must be set on CircleCI_:
These may be set manually or by running the script ``./.circleci/envvars.sh``.

- ``TWINE_USERNAME``: Username for publishing on PyPI.
- ``TWINE_PASSWORD``: Password for publishing on PyPI.
- ``CODECOV_TOKEN``: Codecov token for uploading coverage reports (optional).

Codecov
~~~~~~~

If set, CircleCI_ will send code coverage reports to Codecov_.

- ``CODECOV_TOKEN``: Codecov token for uploading coverage reports.

Docker Hub
~~~~~~~~~~

If set, CircleCI_ will build, tag, and push images to `Docker Hub`_.

- ``DOCKERHUB_REPOSITORY``: Docker Hub repository name.
- ``DOCKERHUB_USERNAME``: Docker Hub username.
- ``DOCKERHUB_PASSWORD``: Docker Hub password.

Bintray
~~~~~~~

If set, CircleCI_ will build, tag, and push images to Bintray_.

- ``BINTRAY_REGISTRY``: Bintray registry name.
- ``BINTRAY_REPOSITORY``: Bintray repository name.
- ``BINTRAY_USERNAME``: Bintray username.
- ``BINTRAY_PASSWORD``: Bintray password (your API key).

Amazon EC2 Container Registry (ECR)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If set, CircleCI_ will build, tag, and push images to `Amazon ECR`_.

- ``AWS_ECR_REPOSITORY``: Amazon ECR repository name.
- ``AWS_ACCOUNT_ID``: Amazon account ID.
- ``AWS_DEFAULT_REGION``: AWS region.
- ``AWS_ACCESS_KEY_ID``: AWS access key ID.
- ``AWS_SECRET_ACCESS_KEY``: AWS secret access key.

Heroku
~~~~~~

If set, CircleCI_ will deploy images built from master directly to Heroku_.

- ``HEROKU_APP``: Heroku application name.
- ``HEROKU_TOKEN``: Heroku authentication token.

.. _Amazon ECR: https://aws.amazon.com/ecr/
.. _Bintray: https://bintray.com/
.. _CircleCI: https://circleci.com/
.. _CircleCI: https://circleci.com/
.. _Codecov: https://codecov.io/
.. _Docker Hub: https://hub.docker.com/
.. _Heroku: https://www.heroku.com/

Docker
~~~~~~

The production Docker image is built on CircleCI from `.circleci/Dockerfile`:
this Dockerfile can only be used with the CircleCI workflow.

In rare cases, building an equivalent container locally may be useful.
Build and run this local container with


::

    $ docker build -t makenew/python-app .
    $ docker run --read-only --init --publish 80:8080 makenew/python-app

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
