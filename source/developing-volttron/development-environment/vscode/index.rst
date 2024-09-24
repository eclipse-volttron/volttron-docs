.. _VSCode-Dev-Environment:

===============================
VSCode Development Environment
===============================

Before setting up the VSCode development environment, ensure the following prerequisites are met:

  1. A Linux environment on WSL2 with necessary software installed. Refer to :ref:`Install WSL2 Ubuntu environment <Install-WSL2-Ubuntu>` for setting up a compatible Linux environment.
  2. Your own fork of the relevant VOLTTRON repositories cloned in your WSL2 environment and poetry environment setup. Refer to :ref:`Forking repository <Fork-Repository>`

VSCode is a versatile Integrated Development Environment (IDE) that supports Python development and offers extensive debugging tools and GitHub integration. It is widely used for developing VOLTTRON projects.

Microsoft provides VSCode as a free download from https://code.visualstudio.com/

Install VSCode
==============
VSCode can be installed directly on your Windows host and configured to connect to code within the WSL2 environment.

**Installing VSCode on Windows:**
 - Download the VSCode installer for Windows from the official site and follow the installation prompts.
 - Once installed, open VSCode and install the **Remote - WSL** extension from the marketplace. This extension allows VSCode to connect and interact with Linux distributions installed via WSL2.

**Configuring WSL2 with VSCode:**
 - Open VSCode.
 - Use the command palette (`Ctrl+Shift+P`) and select **Remote-WSL: New Window**. This opens a new VSCode window directly connected to your WSL2 environment.
 - Navigate to the folder containing your cloned VOLTTRON repositories by selecting **File > Open Folder** and navigating to your project directory in WSL2.

.. note::

    If you are working with multiple WSL2 instances, please refer to the official Visual Studio Code documentation on :doc:`Working with multiple WSL2 distributions <remote-wsl>`.


VSCode Settings/Configurations
==============================
**Setting Up the Python Interpreter:**
 
 - Once in the WSL2 environment, open the command palette and select **Python: Select Interpreter**.
 - Choose the Python interpreter from your VOLTTRON virtual environment. This is typically located in your project's `.venv` directory or wherever your Python virtual environment is set up.

**Install Python and Essential Extensions:**
 
 - Ensure Python is installed in your WSL2 environment using the following command:

   .. code-block:: bash

       sudo apt install python3 python3-pip python3-venv

 - Install essential VSCode extensions such as **Python** and **Pylance** for improved code analysis and IntelliSense.

**Configure Path to the VOLTTRON Source:**

 - Open your VOLTTRON project folder in VSCode to automatically recognize and index the source files.
 - Your `pyproject.toml` file should be visible at the root of the project, enabling VSCode to recognize project dependencies.

**Environment and Editor Settings in settings.json:**

The `settings.json` file in VSCode is crucial for customizing the IDE environment to fit the needs of VOLTTRON
development. The settings might include paths to data directories, specific Python paths, and integration with GIT
features, enhancing workflow efficiency and accessibility. Here is a code snippet example of the `settings.json` configuration.

.. code-block:: json
    
   {
        "terminal.integrated.env.linux": {
            "PYTHONPATH": "${workspaceFolder}/src/:${env:PYTHONPATH}",
            "VOLTTRON_HOME": "/home/${env:USER}/.volttron_modular"
        },
        "editor.formatOnSave": true,
        "python.analysis.typeCheckingMode": "basic",
        "editor.rulers": [
            88,
            120
        ],
        "python.analysis.extraPaths": [
            "${workspaceFolder}src/",
        ],
    }


**Debugging and Run Configurations in launch.json:**

The `launch.json` file is used to set up and customize debugging configurations. This file defines how VSCode should
launch and debug your VOLTTRON applications, including settings for environment variables, Python paths, and specific
commands or scripts to run. Here is a code snippet example of the `launch.json` configuration.

.. code-block:: json
    
   {
        "configurations": [
            {
                "name": "volttron -vv",
                "type": "python",
                "request": "launch",
                "program": ".venv/bin/volttron",
                "console": "integratedTerminal",
                "justMyCode": true,
                "args": [
                    "-vv",
                    "--dev",
                    "-l",
                    "volttron.log",
                    "--log-config",
                    "logging_config.yaml"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "launch volttron-listener",
                "type": "debugpy",
                "request": "launch",
                "program": "/home/os2204/repos/volttron-redo/volttron-listener/src/listener/agent.py",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "justMyCode": true,
                "args": [
                    "-vv",
                    "--json",
                    "start",
                    "volttron-listener-0.2.0rc0"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                    "AGENT_CREDENTIALS": "/home/os2204/.volttron_redo/credentials_store/volttron-listener-0.2.0rc0_2.json",
                    "AGENT_VIP_IDENTITY": "volttron-listener",
                    //"AGENT_VIP_IDENTITY": "volttron-listener-0.2.0rc0_2",
                    "VOLTTRON_PLATFORM_ADDRESS": "ipc://@/home/os2204/.volttron_redo/run/vip.socket"
                    //"VOLTTRON_PLATFORM_ADDRESS": "tcp://127.0.0.1:22916"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
        ]
    }

.. note::

    - Most VOLTTRON functions are done within a greenlet and hence GEVENT_SUPPORT is a required environment variable to
      effectively debug VOLTTRON server and agent functions.
    - VOLTTRON_HOME environment variable is optional (defaults to ~/.volttron) but if set in launch configuration of
      volttron server, make sure to point to the same value for agents', or vctl's launch configurations


This configuration allows developers to efficiently run and debug VOLTTRON applications using specific environment
settings and utilities directly from VSCode, leveraging the powerful coding assistance and debugging tools provided by the IDE.
