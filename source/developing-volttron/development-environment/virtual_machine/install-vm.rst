.. _Install-VM:

==================================
Installing a Linux Virtual Machine
==================================

VOLTTRON requires a Linux system to run. For Windows users this will require a virtual machine (VM), a docker container,
or a WSL2 environment

This section describes the steps necessary to install VOLTTRON using Oracle VirtualBox software. Virtual Box is
free and can be downloaded from https://www.virtualbox.org/wiki/Downloads.

|VirtualBox Download|

.. |VirtualBox Download| image:: files/vbox-download.png

After installing VirtualBox download a virtual box appliance from https://www.osboxes.org/ extract the
VDI from the downloaded archive, **or** download a system installation disk. VOLTTRON version 10.x has been tested
using Ubuntu 22.04. However, any modern apt based Linux distribution should work out of the box.

Linux Mint 19.3 with the Xfce desktop is used as an example, however platform setup in Ubuntu should be identical.

.. note::

    A 32-bit version of Linux should be used when
    running VOLTTRON on a system with limited hardware (less than 2 GB of RAM).


Adding a VDI Image to VirtualBox Environment
********************************************

|Linux Mint|

.. |Linux Mint| image:: files/linux-mint.png


The below info holds the VM's preset username and password.

|Linux Mint Credentials|

.. |Linux Mint Credentials| image:: files/vbox-credentials.png

Create a new VirtualBox Image.

|VirtualBox VM Naming|

.. |VirtualBox VM Naming| image:: files/vbox-naming.png


Select the amount of RAM for the VM. The recommended minimum is shown in the image below:

|VirtualBox Memory Size Selection|

.. |VirtualBox Memory Size Selection| image:: files/vbox-memory-size.png

Specify the hard drive image using the extracted VDI file.

|VirtualBox Hard Disk|

.. |VirtualBox Hard Disk| image:: files/vbox-hard-disk-xfce.png

With the newly created VM selected, choose Machine from the VirtualBox menu in the top left corner of the VirtualBox
window; from the drop down menu, choose Settings.

To enable bidirectional copy and paste, select the General tab in the VirtualBox Settings. Enable Shared Clipboard and
Drag’n’Drop as Bidirectional.

|VirtualBox Bidirectional|

.. |VirtualBox Bidirectional| image:: files/vbox-bidirectional.png

.. note::
    Currently, this feature only works under certain circumstances (e.g. copying / pasting text).

Go to System Settings. In the processor tab, set the number of processors to two.

|VirtualBox Processors|

.. |VirtualBox Processors| image:: files/vbox-proc-settings.png


Go to Storage Settings. Confirm that the Linux Mint VDI is attached to Controller: SATA.


.. DANGER::
    Do **NOT** mount the Linux Mint iso for Controller: IDE. **Will result in errors.**

|VirtualBox Controller|

.. |VirtualBox Controller| image:: files/vbox-controller.png

Start the machine by saving these changes and clicking the “Start” arrow located on the upper left hand corner of the
main VirtualBox window.


Install VOLTTRON pre-requisites
*******************************
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
