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

The first step to editing any volttron repository is to fork it into your own user space.  Creating a fork makes a copy
of the repository in your GitHub for you to make any changes you may require for your use-case.  This allows you to make
changes without impacting the core VOLTTRON repository.

VOLTTRON platform code is split into multiple repositories one for each customizable core feature. At a minimum, to
run VOLTTRON you would need code from three repositories

  1. http://github.com/eclipse-volttron/volttron-core - which contains VOLTTRON server, client (base agent), commands,
     utilities
  2. http://github.com/eclipse-volttron/volttron-lib-zmq - which contains the ZMQ message bus related code

  3. http://github.com/eclipse-volttron/volttron-lib-auth - which requires authentication and authorization logic

VOLTTRON agents and libraries are also maintained in individual repositories under http://github.com/eclipse-volttron

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

Please refer to :ref:`Setup VOLTTRON for development <Setup-Volttron-Dev>` on how to setup a virtual environment, and
install editable volttron agents and packages and run volttron with it.

Adding and Committing files
===========================
When you make modifications or creating new files to cloned repository, you should periodically (or after logical unit
of work) move these code to git repository. First, you should move the changed file to the stage for review
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
