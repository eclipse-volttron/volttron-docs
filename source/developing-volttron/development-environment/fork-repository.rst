.. _Fork-Repository:

======================
Forking the Repository
======================

Pre-requisites
==============

This document assumes you already have
  1. A Linux environment - This can be a Linux machine, :ref:`a virtual machine <Install-VM>` or
     :ref:`a docker container <Install-WSL2-Ubuntu>`.

  2. VOLTTRON Pre-requisites software - Refer: :ref:`VOLTTRON Pre-requisites <VOLTTRON_Pre-requisites>`

The first step to editing the repository is to fork it into your own user space.  Creating a fork makes a copy of the
repository in your GitHub for you to make any changes you may require for your use-case.  This allows you to make
changes without impacting the core VOLTTRON repository.

VOLTTRON platform code is split into multiple repositories one for each customizable core feature. At a minimum, to
run VOLTTRON you would need code from two repositories

  1. http://github.com/eclipse-volttron/volttron-core - which contains VOLTTRON server, client (base agent), commands,
     utilities
  2. http://github.com/eclipse-volttron/volttron-lib-zmq - which contains the ZMQ message bus related code

If you want to enable authentication and authorization, you would also need

  3. http://github.com/eclipse-volttron/volttron-lib-auth


Fork all repositories that you wish to update. To fork a repository, point your favorite web browser to the
repository, for example http://github.com/eclipse-volttron/volttron-core and then click "Fork" on the upper right of
the screen.  (Note: You must have a GitHub account to fork the repository. If you don't have one, we encourage you to
`sign up <https://github.com/join?source_repo=eclipse-volttron%2Fvolttron-core>`_.)

.. note::

   After making changes to your repository, you may wish to contribute your changes back to the Core VOLTTRON
   repository.  Instructions for contributing code may be found :ref:`here <Contributing-Code>`.


Cloning 'YOUR' VOLTTRON forked repository
=========================================

The next step in the process is to copy your forked repository onto your computer to work on.  This will create an
identical copy of the GitHub repository on your local machine.  To do this you need to know the address of your
repository.  The URL to your repository address will be ``https://github.com/<YOUR GITHUB USERNAME>/<repo name>.git``.
For example, ``https://github.com/github_user1/volttron-core.git``

From a terminal execute the following commands:

.. code-block:: bash

    # Here, we are assuming you are doing develop work in a folder called `git`.
    mkdir -p ~/git
    cd ~/git
    git clone -b develop https://github.com/<YOUR USERNAME>/<repository-name>.git
    cd <repository-name>

.. note::

  VOLTTRON uses develop as its main development branch rather than the standard `main` branch (the default).

Running VOLTTRON using your modified code
=========================================

VOLTTRON uses poetry for dependency management. If your environment does not have poetry, install poetry. Please
refer to `official poetry documentation <https://python-poetry.org/docs/#installing-with-the-official-installer>`_

Once you have poetry installed, do the following to start VOLTTRON using cloned source code

1. Create a poetry project. There are two ways to do this

   a. You could create your own poetry project and add libraries needed

      - Create a new poetry project - (``mkdir <new project dir>; cd <project dir>; poetry init``)
      - Activate poetry shell - ``poetry shell``
      - Add necessary volttron packages using the command ``poetry add <cloned path orp pypi library name>``.
        For example, ``poetry add <path to your cloned volttron-core fork dir>``,
        ``poetry add volttron-lib-zmq``

   or

   b. Use volttron-zmq wrapper

      - Clone the `volttron-zmq library <https://github.com/eclipse-volttron/volttron-zmq>`_ that is a wrapper that is
        dependent on volttron-core, volttron-lib-auth, and volttron-lib-zmq
      - Update pyproject.toml file of volttron-zmq to point to cloned source directory of volttron-core,
        and/or volttron-lib-auth, and/or volttron-lib-zmq

2. Update poetry configuration to set the default location of poetry virtual environments -
   ``poetry config virtualenvs.in-project true``

3. Run ``poetry install`` if you used option a or ``poetry install --no-root`` if you used option b above

4. export VOLTTRON_HOME=/path/to/volttron/home. **Note: VOLTTRON10 cannot work with volttron home directory used for
   previous versions of VOLTTRON**

5. Start VOLTTRON in developer mode using **--dev** option and run it in the backgroun. --dev tells VOLTTRON to use
   the current poetry project and not create a new one in VOLTTRON_HOME.
   Example command: ``volttron --dev -vv -l ./volttron.log &``

6. You can check the status by running the command ``vctl status``

7. To install agents for testing use the vctl install command. This will add the source library of the agent to the
   current poetry project and create agent's data directory in $VOLTTRON/agents. You can use vctl install with agent
   library name fro pypi or to a cloned agent repository

Note:

To debug your source code during development, you could run/debug volttron and vctl commands from within an IDE.
Refer: :ref:`PyCharm development environment<Pycharm-Dev-Environment>`


Adding and Committing files
===========================
When you make modifications or creating new files to cloned repository, you should periodically (or after logical unit
of work) you should move these code git repository. First, you should move the changed file to the stage for review
before committing to the local repository.  For this example let's assume we have made a change to `README.md` in the
root of the volttron directory and added a new file called `foo.py`.  To get those files in the staging area
(preparing for committing to the local repository) we would execute the following commands:

.. code-block:: bash

    git add foo.py
    git add README.md

    # Alternatively in one command
    git add foo.py README.md

After adding the files to the stage you can review the staged files by executing:

.. code-block:: bash

    git status

Finally, in order to commit to the local repository we need to think of what change we actually did and be able to
document it.  We do that with a commit message (the -m parameter) such as the following.

.. code-block:: bash

    git commit -m "Added new foo.py and updated copyright of README.md"


Pushing to the remote repository
================================

The next step is to share our changes with the world through GitHub.  We can do this by pushing the commits
from your local repository out to your GitHub repository.  This is done by the following command:

.. code-block:: bash

    git push

Contribute code
===============
As a open source project, we welcome community contribution of code. If you wish to contribute your changes back to
the Core VOLTTRON repository, please follow the instructions :ref:`here <Contributing-Code>`.
