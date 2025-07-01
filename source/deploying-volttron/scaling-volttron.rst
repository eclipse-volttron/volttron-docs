================
Scaling VOLTTRON
================

VOLTTRON can be used at scale by installing multiple instances of VOLTTRON at multiple host machines.
VOLTTRON provides tools and functionalities to support such a distributed deployment.

Automated Deployment
====================
VOLTTRON provides recipes that leverages `ansible <https://docs.ansible.com/ansible/latest/index.html>`_ to
orchestrate the deployment and configuration process for VOLTTRON, enabling repeatable and consistent deployments across
various host machines. Please see :ref:`volttron ansible documentation <VOLTTRON-ANSIBLE>` for more details.

Federated Service
=================

VOLTTRON provides ability for multiple instances to be part of a federated group.
VOLTTRON provides a federation service, through which various VOLTTRON instances
can register itself to an external platform-lookup or federation registry service and dynamically discover new instances
added to the federation. Federated instances of VOLTTRON can communicate with each other through publish and subscribe
mechanism. Please refer to :ref:`federation documentation <Volttron-Federation>` for more details.

