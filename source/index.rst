.. VOLTTRON documentation root file

=========================
|VOLTTRON|  documentation
=========================

|VOLTTRON Tagline|

|VOLTTRON| is an open source, scalable, and distributed platform that seamlessly integrates data, devices, and
systems for sensing and control applications.  It is built on extensible frameworks allowing contributors to easily
expand the capabilities of the platform to meet their use cases.  Features are implemented as loosely coupled software
components, called agents, enabling flexible deployment options and easy customization.

The VOLTTRON project is now officially part of the Eclipse Foundation. Being part of the foundation provides the
governance and support infrastructure to build a vendor-neutral, open source ecosystem that gives all stakeholders the
opportunity to contribute and set technical direction. All new development and releases will be done through the
Eclipse VOLTTRON project. Refer to :ref:`Community Engagement<Community>` to find the different ways to be a part of,
and engage with the Eclipse VOLTTRON community.

Key Use-Cases
=============

- Developing scalable, reusable applications to deploy in the field without spending development resources on
  operational components not specific to the application
- Low-cost data collection deployable on commodity hardware
- Integration hub for connecting a diverse set of devices together in a common interface
- Testbed for developing applications for a simulated environment


.. image:: files/volttron_diagram.png

Features
========

- A :ref:`message bus <Message-Bus>` allowing connectivity between agents on individual platforms and
  between platform instances in large scale deployments
- Integrated security features enabling the management of secure communication between agents and platform instances
- A flexible :ref:`agent framework <Agent-Framework>` allowing users to adapt the platform to their unique use-cases
- A configurable :ref:`driver framework <Driver-Framework>` for collecting data from and sending control
  signals to buildings and devices
- automatic data capture and retrieval through our :ref:`historian framework <Historian-Framework>`
- An extensible :ref:`web framework <Web-Framework>` allowing users and services to securely connect to the platform
  from anywhere
..

- Capability to interface with simulation engines and applications to evaluate applications prior to deployment


VOLTTRON™ is publicly available from `GitHub <https://github.com/eclipse-volttron/volttron-core.git>`_ and
`PyPI <https://pypi.org/project/volttron/>`_. The project is supported by the U.S. Department of Energy and
receives ongoing updates from a team of core developers at PNNL.  The VOLTTRON team encourages and appreciates
community involvement including issues, pull requests, discussions on Github, meetings at our bi-weekly office-hours,
and quaterly user meetings. To be invited to office-hours, please `send the team an email
<volttron-dev@eclipse.org>`_.

.. toctree::
   :caption: Introduction
   :hidden:
   :titlesonly:
   :maxdepth: 1

   introduction/platform-install
   introduction/definitions
   introduction/license

.. toctree::
   :caption: Platform Features
   :hidden:
   :titlesonly:
   :maxdepth: 1

   platform-features/message-bus/index
   platform-features/control/index
   platform-features/config-store/configuration-store
   platform-features/security/volttron-security
   external-docs/volttron-lib-web/index

.. toctree::
   :caption: Agent Framework
   :hidden:
   :titlesonly:
   :maxdepth: 1

   agent-framework/agents-overview
   agent-framework/platform-service-standardization
   external-docs/volttron-platform-driver/index
   external-docs/volttron-lib-base-historian/index
   external-docs/volttron-lib-tagging/index

.. toctree::
   :caption: Developing in VOLTTRON
   :hidden:
   :titlesonly:
   :maxdepth: 1

   developing-volttron/community
   developing-volttron/development-environment/index
   developing-volttron/developing-agents/agent-development
   developing-volttron/contributing-code
   developing-volttron/contributing-documentation

.. toctree::
   :caption: Deploying VOLTTRON
   :hidden:
   :titlesonly:
   :maxdepth: 1

   deploying-volttron/platform-configuration
   deploying-volttron/deployment-planning-options
   deploying-volttron/secure-deployment-considerations
   deploying-volttron/linux-system-hardening

.. toctree::
   :caption: VOLTTRON Core Agents
   :hidden:
   :titlesonly:
   :maxdepth: 2
   :glob:

   SQLiteHistorian <external-docs/volttron-sqlite-historian/index>
   PostgresqlHistorian <external-docs/volttron-postgresql-historian/index>
   SQLiteTaggingAgent <external-docs/volttron-sqlite-tagging/index>

.. toctree::
   :caption: VOLTTRON Application Agents
   :hidden:
   :titlesonly:
   :maxdepth: 2
   :glob:

   Intelligent Load Controller <external-docs/volttron-ilc/index>
   Economizer RCx <external-docs/volttron-economizer-rcx/index>

.. toctree::
   :caption: VOLTTRON Operational Agents
   :hidden:
   :titlesonly:
   :maxdepth: 2
   :glob:

   Topic Watcher <external-docs/volttron-topic-watcher/index>
   Threshold detection <external-docs/volttron-threshold-detection/index>
   Sysmon <external-docs/volttron-sysmon/index>
   Log statistics <external-docs/volttron-log-statistics/index>

.. toctree::
   :caption: VOLTTRON Releases
   :hidden:
   :titlesonly:
   :maxdepth: 1

   Releases <volttron-topics/VOLTTRON-releases/index>

..

   volttron-topics/troubleshooting/index
   volttron-topics/volttron-applications/index



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

.. |VOLTTRON| unicode:: VOLTTRON U+2122
.. |VOLTTRON Tagline| image:: files/VOLLTRON_Logo_Black_Horizontal_with_Tagline.png
