.. _Platform-Installation:

.. role:: bash(code)
   :language: bash

=======================
Installing the Platform
=======================

VOLTTRON is written in Python 3.10+ and runs on Linux Operating Systems.  For users unfamiliar with those technologies,
the following resources are recommended:

-   `Python 3.10 Tutorial <https://docs.python.org/3.10/tutorial>`_
-   `Linux Tutorial <http://ryanstutorials.net/linuxtutorial>`_

This guide will specify commands to use to successfully install the platform on supported Linux distributions, but a
working knowledge of Linux will be helpful for troubleshooting and may improve your ability to get more out of your
deployment.

.. note::

    This version of VOLTTRON was tested by the VOLTTRON core team on Ubuntu 22.04 with python 3.10


.. _Platform-Prerequisites:

Step 1 - Install prerequisites
==============================

The following packages will need to be installed on the system:

*  python >= 3.10
*  pip
*  poetry >= 2.0.1

Verify python installation with the following command:

.. code-block:: bash

       $ python3 --version

.. code-block:: bash

       # expected output similar to this
       Python 3.10.6


Install the dependencies with the following command:

.. code-block:: bash

       $ sudo apt install python3-venv python3-pip

Install poetry:

Please refer to `official poetry documentation <https://python-poetry.org/docs/#installing-with-the-official-installer>`_

After install of poetry, we recommend updating poetry configuration to create virtual environment within the project. This is especially useful if you plan to use  poetry to build volttron libraries from source and develop agents or contribute to volttron core. 

.. code-block:: bash

   $ poetry config virtualenvs.in-project true



Step 2 - (Optional) Create and activate virtual environment
===========================================================
This step is not required if running on a isolated environment such as docker container or virtual machine. However,
when installing VOLTTRON on a machine that is used for multiple projects/software, it is highly recommended that you
create a virtual python environment within which VOLTTRON is installed and executed. This would isolate VOLTTRON and
its dependencies from overwriting or creating version inconsistencies with other python libraries installed at
system level.
Use the below commands to create a python virtual environment and activate it.

.. code-block::

    python3 -m venv /path/to/new/virtual/environment
    source  /path/to/new/virtual/environment/activate


You may notice the command prompt has changed and there is the virtual environment name as prefix.
e.g., :code:`(volttron) user@host:~/volttron $`. The prefix environment name indicates the virtual environment
is activated.

Alternatively, you can use the following command to verify if the virtual environment is up.

.. code-block:: bash

       $ env |grep VIRTUAL_ENV |wc -l

.. code-block:: bash

       # expected output 1(virtual environment is up) or 0 (not up)


Use `deactivate` command to deactivate the virtual environment. NOTE: if you run this command, remember to re-activate
the virtual environment to follow the rest of the steps.


Step 3 - Install VOLTTRON
=========================

Run the command

.. code-block::

    pip install volttron

This pulls the latest stable version of volttron from pypi. If needed, you specify the version of volttron using
`version specifiers <https://pip.pypa.io/en/stable/reference/requirement-specifiers/>`_

Step 4. Setup VOLTTRON_HOME (optional)
======================================
In the above step we installed all source code of VOLTTRON into the virtual environment's python environment.
Each VOLTTRON instance stores its instance specific data - ports used, agents installed, service enabled etc. - in a
VOLTTRON_HOME directory. The default value for this is <user home>/.volttron.

You can set a different destination for your volttron instance using the environment variable
VOLTTRON_HOME. For example,

.. code-block:: bash

    export VOLTTRON_HOME=/path/to/my/volttron/instance

Step 5. Start VOLTTRON
======================

We are now ready to start VOLTTRON instance.

The following command starts volttron process in the background:

.. code-block:: bash

  volttron -vv -l volttron.log&

This enters the virtual Python environment and then starts the platform in debug (vv) mode with a log file
named volttron.log. By default log file will get written to VOLTTRON_HOME directory. During the first volttron run for
a volttron instance, volttron creates a poetry project inside VOLTTRON_HOME directory ($VOLTTRON_HOME/pyproject.toml)
and uses that manage all volttron packages.

.. warning::
    If you plan on running VOLTTRON in the background and detaching it from the
    terminal with the ``disown`` command be sure to redirect stderr and stdout to ``/dev/null``.
    Some libraries which VOLTTRON relies on output directly to stdout and stderr.
    This will cause problems if those file descriptors are not redirected to ``/dev/null``

    ::

        #To start the platform in the background and redirect stderr and stdout
        #to /dev/null
        volttron -vv -l volttron.log > /dev/null 2>&1&

Check the status of VOLTTRON with the following command:

.. code-block:: bash

       $ vctl status

For fresh installation, the result might look like the following since there are no agents installed yet.

.. code-block:: bash

       # expected output similar to this
       No installed Agents found

.. tip::

    Use :code:`vctl status` to check status.
    This is a very useful command to inspect the status of VOLTTRON.

.. _installing-and-running-agents:

Step 6. Installing and Running Agents
======================================

Once VOLTTRON is running you can install any volttron agent from PYPI using the `vctl install` command from the same
python environment that is running VOLTTRON. For example. install the listener agent using the command

.. code-block:: bash

    vctl install volttron-listener

This pulls the volttron-listener package from pypi and creates a volttron agent instance with a auto generated unique
vip identity. Optionally you can specify the vip-identity as command line parameters. You could also add a tag to the
agent

For example:

.. code-block:: bash

  vctl install volttron-listener --vip-identity volttron-listener-agent-1 --tag listener

.. code-block:: bash

       # expected output similar to this
       Agent b755bae2-a3f5-44a0-b01f-81e30b989138 installed

Check the status of install agent using

.. code-block:: bash

    vctl status

Start the agent using the uuid or tag

.. code-block:: bash

    vctl start --tag listener

.. code-block:: bash

       # expected output similar to this
       Starting b755bae2-a3f5-44a0-b01f-81e30b989138 listeneragent-3.3

You can  use the `volttron-ctl` (or `vctl`) command to start, stop or check the status of an agent

.. code-block:: console

    (volttron)volttron@volttron1:~/git/rmq_volttron$ vctl status
      AGENT                  IDENTITY            TAG           STATUS          HEALTH
    6 listeneragent-3.2      listeneragent-3.2_1               running [13125] GOOD
    f platform_driveragent-3.2 platform.driver     platform_driver

.. code-block:: bash

    vctl stop <agent id>


.. note::

    The default working directory is ~/.volttron. The default directory for creation of agent packages is
    `~/.volttron/agents`


In addition to the :code:`vctl status`, another way to check VOLTTRON status is by inspecting
the :code:`volttron.log` file. The file provides rich information about the platform and becomes handy for
debug purposes.

.. code-block:: bash

       $ tail -f volttron.log


.. code-block:: bash

       # example output (success)
       # listener agent is publishing heartbeat messages successively.
       2022-03-04 14:12:46,463 (listeneragent-3.3 2192) __main__ INFO: Peer: pubsub, Sender: listeneragent-3.3_1:, Bus: , Topic: heartbeat/listeneragent-3.3_1, Headers: {'TimeStamp': '2022-03-04T19:12:46.460096+00:00', 'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 'GOOD'
       ...


.. code-block:: bash

       # example output (error)
       2022-03-04 13:16:05,469 (listeneragent-3.3 3233) volttron.platform.vip.agent.core ERROR: No response to hello message after 10 seconds.
       2022-03-04 13:16:05,469 (listeneragent-3.3 3233) volttron.platform.vip.agent.core ERROR: Type of message bus used zmq
       2022-03-04 13:16:05,469 (listeneragent-3.3 3233) volttron.platform.vip.agent.core ERROR: A common reason for this is a conflicting VIP IDENTITY.
       2022-03-04 13:16:05,469 (listeneragent-3.3 3233) volttron.platform.vip.agent.core ERROR: Another common reason is not having an auth entry onthe target instance.
       2022-03-04 13:16:05,469 (listeneragent-3.3 3233) volttron.platform.vip.agent.core ERROR: Shutting down agent.
       ...

Step 7. Installing VOLTTRON libraries (Optional)
=================================================

To install any volttron libraries needed by use the ``vctl install-lib <pypi package or src dir>`` command. For example,

.. code-block:: bash

    vctl install-lib /path/to/cloned/volttron-lib-bacnet-driver
    vctl install-lib volttron-lib-bacnet-driver

Step 7. Stop VOLTTRON (Optional)
================================

To stop VOLTTRON, use the following command:

.. code-block:: bash

       $ vctl shutdown --platform

.. code-block:: bash

       # expected output similar to this
       Shutting down VOLTTRON

After stopping the platform, check the status again to verify the VOLTTRON platform is shut down.

.. code-block:: bash

       $ vctl status

.. code-block:: bash

       # expected output similar to this
       VOLTTRON is not running. This command requires VOLTTRON platform to be running

Clean up (Optional)
====================

If for some reason you would like to clean up VOLTTRON, here is the guide to remove the whole VOLTTRON package

- remove code. For example, `pip uninstall volttron` or delete entire virtual environment of volttron
`deactivate;rm -rf /path/to/volttron/venv`
- remove VOLTTRON data directory - `rm -rf $VOLTTRON_HOME`

Next Steps
==========
You can explore the list of available agents by searching PYPI for "volttron-". The core VOLTTRON team maintains several
commonly used agents such as Platform drivers and Historians. This website provides links to all the core agents
documentation. You can get a overview of the agent frameworks at :ref:`Agent Framework <Agent-Framework>`.

:ref:`Planning Deployment <Planning-Deployments>`, :ref:`Linux System Hardening <Linux-System-Hardening>`,
and :ref:`VOLTTRON security considerations<VOLTTRON-Security>` explain factors to consider when deploying
VOLTTRON for production environments
