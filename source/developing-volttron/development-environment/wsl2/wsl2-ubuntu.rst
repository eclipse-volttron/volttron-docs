.. _Install-WSL2-Ubuntu:

====================================
Install Ubuntu using wsl2 on Windows
====================================

VOLTTRON requires a Linux system to run. For Windows users this will require a virtual machine (VM), a docker container,
or a WSL2 environment. This document covers the details about setting up a Ubuntu environment using wsl2 on Windows 10
or Windows 11

Install/Enable WSL2
-------------------

If you are running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11, wsl2 should already
be enabled on your system and you can directly proceed to installing a linux environment using wsl2.
If you are on a older Windows machine you will have first enable wsl. Please refer to
`this microsoft documentation <https://learn.microsoft.com/en-us/windows/wsl/install-manual>`__ to manually enable wsl
and check if you have the required minimum build for enabling wsl2

Terminal Application
--------------------

We highly recommend a good terminal emulator such as the latest version of Microsoft Terminal or Cmder or similar that
provides features such as multiple tabs, search, etc. This would come handy for development of VOLTTRON code base.


Install Ubuntu 22.04 with WSL
-----------------------------

The current version of Eclipse VOLTTRON has been tested on Ubuntu 22.04 so this document refers that specific
distribution. You are free to use other Linux distributions but please note that there would minor changes in package
names and available versions of dependency.

To install Ubuntu 22.04 with wsl2, open PowerShell or Windows Command Prompt or similar in administrator mode and run
the following command

.. code-block:: bash
    wsl.exe --install -d Ubuntu-22.04

Note: You can find out the available linux environments that can be installed, use the command
``wsl --list --online``

Setup Ubuntu environment
------------------------

1. Open installed Ubuntu environment by going to the start menu and typing Ubuntu and selecting Ubuntu-22.04. Or you
   could run the command ``wsl -d Ubuntu-22.04`` from command prompt of your terminal emulator

2. When you open the distribution for the first time, you would be prompted to create a linux user name and password.
   This account will be your default user for the distribution and automatically sign-in on launch. THis account will
   also be considered admin account and will have sudo access

3. Update and upgrade packages using the command ``sudo apt update && sudo apt upgrade``

.. _VOLTTRON_Pre-requisites:
Install VOLTTRON pre-requisites
-------------------------------
Once you login into your virtual machine, install VOLTTRON pre-requisite softwares in your linux environment. VOLTTRON
requires the following software

1. python 3.10 (official version tested)
2. git
3. python3-venv
4. poetry

Ubuntu-22.04 comes with python 3.10 and git.

- If not installed, use the command ``sudo apt install python3.10`` to install python3.10

- If not installed, use the command ``sudo apt install git`` to install git

- Install python venv for python 3.10 using the command ``sudo apt-get install python3.10-venv``

- VOLTTRON uses poetry for dependency management. For development environments, it is required that
  you install poetry, and use poetry commands to create virtual environment and install volttron source packages

    1. Run the command `` curl -sSL https://install.python-poetry.org | python3 -`` to install poetry on Ubuntu
    2. Add poetry install directory to your PATH. Open .bashrc file in your home directory and add the following command
       with the correct path to your home directory ``export PATH="<path to your home dir>/.local/bin:$PATH"``
    3. Source .bashrc (only for the first time) - ``source ~/.bashrc``
    4. Update poetry configuration to set the default location of poetry virtual environments -
       ``poetry config virtualenvs.in-project true``




