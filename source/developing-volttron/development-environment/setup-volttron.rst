.. _Setup-Volttron-Dev:
==============================
Setup VOLTTRON for development
==============================

Prerequisites
=============
This document assumes you already have
  1. A Linux environment - This can be a Linux machine, :ref:`a virtual machine <Install-VM>` or
     :ref:`a docker container <Install-WSL2-Ubuntu>`.
  2. VOLTTRON Pre-requisites software - Refer: :ref:`VOLTTRON Pre-requisites <VOLTTRON_Pre-requisites>`
  3. Forked the volttron-* repository you are editing. See :ref:`forking volttron-core for development <Fork-Repository>`

Running VOLTTRON with source code
==================================
  1. Create a new directory, say volttron_instance1
  2. Create a new virtual environment in that directory and activate it

     .. code-block:: bash
         cd volttron_instance1
         python3 -m venv .venv
         source .venv/bin/activate

  3. Install volttron-core, volttron-lib-auth and volttron-lib-zmq.

     If editing one the above three platform packages:
     *************************************************
     You can point to your clone fork directory for the library you are editing and use pypi packages for rest.
     You can do this using pip or poetry

     a. Using pip

        - ``pip install -e <path to cloned volttron-core dir>`` or ``pip install volttron-core``
        - ``pip install -e <path to cloned volttron-lib-auth dir>`` or ``pip install volttron-lib-auth``
        - ``pip install -e <path to cloned volttron-lib-zmq dir>`` or ``pip install volttron-lib-zmq``

     or

     b. Using poetry and volttron-zmq wrapper

        - Clone the `volttron-zmq library <https://github.com/eclipse-volttron/volttron-zmq>`_ that is a wrapper that is
          dependent on volttron-core, volttron-lib-auth, and volttron-lib-zmq
        - Update pyproject.toml file of volttron-zmq to point to cloned source directory of volttron-core,
          and/or volttron-lib-auth, and/or volttron-lib-zmq and mark these source package as editable so that you don't
          have to rebuild the wheel
        - run ``poetry install``

     If editing volttron agent or volttron libraries
     ***********************************************
     If you updating one of volttron agents or volttron-lib-* packages, you can simply install volttron using
     ``pip intall volttron``

  4. Optional: `export VOLTTRON_HOME=/path/to/volttron-home`` Defaults to $HOME/.volttron. **Note: VOLTTRON>= 10
     cannot work with volttron home directory used for previous versions of VOLTTRON**

  5. Start volttron ``volttron -l volttron.log &`` This creates a new poetry project in $VOLTTRON_HOME and use that.

  6. You can check the status by running the command ``vctl status``

  7. To install agents use
     ``vctl install <agent package name in pypi>``
     or
     ``vctl install <path to forked agent source dir>``

  8. To install any optional libraries use the ``vctl install-lib`` command.
     Example:
     ``vctl install-lib volttron-lib-bacnet-driver``
     or
     ``vctl install-lib <path to forked library directory>``

  9. Using ``vctl install`` and ``vctl install-lib`` ensures that versions of python packages used by VOLTTRON are
     all compatible with each other. Using ``pip install <library>`` might work if there is no dependency
     version mismatch but pip doesn't do dependency management as well as poetry.

Note:

To debug your source code during development, you could run/debug volttron and vctl commands from within an IDE.
Refer: :ref:`PyCharm development environment<Pycharm-Dev-Environment>`

After executing the above commands your environment is setup for starting volttron.  The next
step is to begin developing an agent(see :ref:`agent development <Agent-Development>`, or continue on with setting up
pycharm for use with this environment(see :ref:`Pycharm development environment <Pycharm-Dev-Environment>`)

Note: To exit the poetry shell use the exit command. this deactivates the environment and exits the spawned shell.
