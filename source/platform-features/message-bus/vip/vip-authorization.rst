.. _VIP-Authorization:

========================================
VIP Authorization (Modular VOLTTRON)
========================================

:ref:`VIP <VIP-Overview>` (VOLTTRON Interconnect Protocol) authorization in modular VOLTTRON
provides fine-grained access control over what authenticated agents can do on the platform.
Unlike monolithic VOLTTRON where authorization rules were embedded in agent code and auth.json,
modular VOLTTRON separates authorization into a flexible, administrator-configurable system.

For authentication, see :ref:`VIP Authentication <VIP-Authentication>`.

Overview
--------

In modular VOLTTRON, authorization:

- **Is separate from agent code** - Agents don't dictate which methods are protected
- **Is instance-specific** - Different instances of the same agent can have different permissions
- **Uses a Unix-style model** - Agents, groups, roles, and capabilities
- **Is flexible** - Both RPC method calls and pub/sub topics can be protected
- **Is centrally managed** - Platform administrators define all access policies

The authorization framework is defined in abstract classes located in ``volttron-core/types/auth/auth_service.py``,
with concrete implementations in ``volttron-lib-auth/src/volttron/auth/authz_manager.py`` and
message-bus-specific handling in ``volttron-lib-zmq``.

Authorization Rules Persistence
-------------------------------

**authorization rules of a specific instance of volttron is persisted in $VOLTTRON_HOME/authz.json**. On first time start
of a volttron instance a authz.json is created for all service agents. Everytime a agent is installed, in addition to
creating authentication credentials, agents are also given default set of authorization and the entries are persisted in
$VOLTTRON_HOME/authz.json

Authorization Model
-------------------

Unix-Style Hierarchy
~~~~~~~~~~~~~~~~~~~~

Modular VOLTTRON's authorization follows a Unix-inspired hierarchy:

1. **agents** - Similar to Unix users. Represents an authenticated peer (installed agent or service agent or remote agent)
2. **agent_groups** - Similar to Unix groups. Collections of agents that share permissions
3. **Roles** - Named permission sets that can be assigned to agents or agent_groups
4. **Capabilities** - Specific permissions:
   - RPC capabilities: Allow calling specific methods on specific agent instance
   - Pub/Sub capabilities: Allow publishing/subscribing to specific topics

The hierarchy flows like this:

.. code-block:: text

    Agents
      ├── Direct RPC Capabilities
      ├── Direct Pub/Sub Capabilities
      └── Assigned Roles
            ├── RPC Capabilities (from role)
            └── Pub/Sub Capabilities (from role)

    Agent groups
      ├── Member agents
      └── Assigned Roles
            ├── RPC Capabilities (inherited by members)
            └── Pub/Sub Capabilities (inherited by members)

**Example Structure**

.. code-block:: text

    Roles:
      - "admin" → Full RPC + Pub/Sub access
      - "config_manager" → Can call config-store methods
      - "historian_reader" → Can query historian

    Groups:
      - "building_operators" → Agents: [op1, op2] → Roles: [config_manager]
      - "technicians" → Agents: [tech1] → Roles: [historian_reader]

    Agents: Identified by individual agent's vip id
      - agent1.vipid → Groups: [building_operators] → Roles: [historian_reader]
      - platform.historian → Direct rpc capabilities to call insert, query

RPC Method Authorization
------------------------

RPC Authorization Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Protected RPC Methods
~~~~~~~~~~~~~~~~~~~~~

**By default all RPC exported methods are open to call by vip.rpc.call by all agents.** Unlike monolithic volttron,
there is no restriction dictated at source code level. For example, in the below agent
public_method and admin_method are both callable by rpc by all agent. But a volttron instance administrator can choose to
protect one or more rpc methods by declaring it as "protected_rpcs" of a specific instance of the agent

.. code-block:: python

    class MyAgent(Agent):
        @RPC.export
        def public_method(self):
            """Any authenticated agent can call this."""
            pass

        @RPC.export
        def admin_method(self):
            """This method is protected; only authorized agents can call it."""


For example, when I install two instance of the above agent say my-agent

.. code-block:: shell

    vctl install --vip-identity myagent-instance1 my-agent
    vctl install --vip-identity myagent-instance2 my-agent

The corresponding $VOLTTRON_HOME/authz.json entries would be

.. code-block:: json

    "myagent-instance1": {
      "agent_roles": [
        {
          "default_rpc_capabilities": {
            "identity": "myagent-instance1"
          }
        }
      ],
      "comments": "Created during creation of credentials!"
    },
    "myagent-instance2": {
      "agent_roles": [
        {
          "default_rpc_capabilities": {
            "identity": "myagent-instance2"
          }
        }
      ],
      "comments": "Created during creation of credentials!"
    }

To make the admin_method restricted, administrator can edit the file to include "protected_rpcs" list, for example


.. code-block:: json

    "myagent-instance1": {
      "protected_rpcs": ["admin_method"],
      "agent_roles": [
        {
          "default_rpc_capabilities": {
            "identity": "myagent-instance1"
          }
        }
      ],
      "comments": "Created during creation of credentials!"
    },

Or protect the method both instances you can add protected_rpcs entries to both 'myagent-instance1' and 'myagent-instance2'


Granting RPC Permissions to protected methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Platform administrators can grant RPC permissions to protected RPC methods by adding RPCCapabilities directly to
agents, or agent groups or roles and then assigning the role to the agent


Method Naming Convention
************************

RPCCapabilities specify the methods using the format:

.. code-block:: text

    <agent vip identity>.<method name>

For example:

- ``platform.historian.query`` - The query method on the historian with vip id 'platform.historian'
- ``platform.config_store.set_config`` - The set_config method on agent platform.config_store
- ``my_agent.start_scan`` - The start_scan method on agent with vip id my_agent

This enables **instance-specific authorization** - you can protect ``platform.historian.query``
without protecting ``backup_historian.query``.

To grant access to say agent, ``calling-agent-1`` to ``myagent-instance1's admin_method`` (see example in previous section)
edit the entry for ``caling-agent-1`` in $VOLTTRON_HOME/authz.json to add "rpc_capabilities"

Example:
********

.. code-block:: json

    "calling-agent-1": {
     "rpc_capabilities": [
        "myagent-instance1.admin_method"
      ],
      "protected_rpcs": ["calling_agent_protected_method1"],
      "agent_roles": [
        {
          "default_rpc_capabilities": {
            "identity": "calling-agent-1"
          }
        }
      ],
      "comments": "Admin_agent1 added rpc capabilities"
    },



Pub/Sub Authorization
---------------------

Pub/Sub Overview
~~~~~~~~~~~~~~~~

In modular VOLTTRON, pub/sub topics can be protected to control who can **publish** and **subscribe**.
Unlike monolithic VOLTTRON (write-protection only), modular VOLTTRON supports both directions.

**Topic Protection Patterns**

Topics can be protected using:

- **Exact topic names**: ``building/hvac/temperature``
- **Regular expressions**: Expressions should be enclosed in forward slashes - example ``/^building\/[^/]+\/temperature/`` ,  ``/.*/``

Protected Topics
~~~~~~~~~~~~~~~~

By default topics are not protected. To make a topic protected, add it to the list of protected topics in $VOLTTRON_HOME/authz.json
This entry is not specific to a single agent. This is a single list for the entire instance -i.e all protected topics for this volttron instance.
Hence authz entry should be made outside of any agent specific entry. The key "protected_topics" should be at the
same level as "roles", agents, and agent_groups

.. code-block:: python
    {
       "protected_topics" : ["devices/mysensitive-device", "/platform/health",  "/building\\/solar\\/.*/"],
       "roles": {
        "default_rpc_capabilities": {
        "rpc_capabilities": [
            "platform.config_store.initialize_configs",
            "platform.config_store.set_config",
            "platform.config_store.delete_store",
            "platform.config_store.delete_config"
        ]
        },
    }


Pub/Sub Permissions
~~~~~~~~~~~~~~~~~~~

Once a pubsub topic is protected, only agents with explicit subscribe or publish capabilities can access it.

Authorized access rights includes:

- **publish**: Permission to send messages on a topic
- **subscribe**: Permission to receive messages on a topic
- **pubsub**: Both publish and subscribe permissions

Excample: $VOLTTRON_HOME/authz.json entries for ``subscribe-only-agent`` and ``publish-only-agent``


.. code-block:: json

    "subscribe-only-agent": {
        "rpc_capabilities": [
            "myagent-instance1.admin_method"
        ],
        "protected_rpcs": ["subscribe_agents_protected_method1"],
        "pubsub_capabilities": {
            "devices/mysensitive-device": "subscribe"
        },
        "agent_roles": [
            {
            "default_rpc_capabilities": {
                "identity": "subscribe-only-agent"
            }
            }
        ],
        "comments": "Admin_agent1 added rpc capabilities, admin_agent2 added pubsub capabilities"
    },

    "publish-only-agent": {
        "rpc_capabilities": [
            "myagent-instance1.admin_method"
        ],
        "protected_rpcs": ["my_protected_method2"],
        "pubsub_capabilities": {
            "devices/mysensitive-device": "publish"
        },
        "agent_roles": [
            {
            "default_rpc_capabilities": {
                "identity": "subscribe-only-agent"
            }
            }
        ],
        "comments": "Admin_agent1 added rpc capabilities, admin_agent2 added pubsub capabilities"
    },

Working with Roles
-------------------

Roles are named permission sets that encapsulate a collection of RPC and Pub/Sub capabilities.
Roles simplify permission management by allowing you to define permissions once and assign the role
to multiple agents or groups.

**Benefits of Roles**

- **Reusability**: Define permissions once, apply to multiple agents and groups
- **Consistency**: Ensure all members of a role have identical permissions
- **Maintainability**: Update all role members by modifying the role definition
- **Scalability**: Manage permissions at scale using role assignments

**Creating and Managing Roles**

Roles are defined in the ``$VOLTTRON_HOME/authz.json`` file under the "roles" section:

.. code-block:: json

    "roles": {
        "historian_reader": {
            "pubsub_capabilities": {
                "historian/query": "subscribe",
                "historian/results": "subscribe"
            }
        },
        "config_manager": {
            "rpc_capabilities": [
                "platform.config_store.get_config",
                "platform.config_store.set_config"
            ]
        },
        "admin": {
            "rpc_capabilities": [
                "/.*/"
            ],
            "pubsub_capabilities": {
                "/.*/": "pubsub"
            }
        }
    }

**Assigning Roles to Agents and Groups**

Roles are assigned through the ``agent_roles`` property. An agent or group can have multiple roles.

Assigning to a single agent:

.. code-block:: json

    "my_agent": {
        "agent_roles": ["historian_reader", "config_manager"]
    }

Assigning role to a group: Example: assigning role to group ``operators``

.. code-block:: json

    "agent_groups": {
        "operators": {
            "identities": ["operator1", "operator2"],
            "agent_roles": [ "config_manager"]
        }
    }


Working with Groups
-------------------

Groups enable managing permissions for multiple agents at once. To create an agent group, add a group under "agent_groups"
in ``$VOLTTRON_HOME/authz.json`` and add a list of agent identities to it. By default VOLTTRON creates an admin group that
can be used as an example

.. code-block:: json

    "agent_groups": {
        "admin": {
        "identities": [
            "platform.federation",
            "control.connection",
            "platform.health",
            "platform.control",
            "platform",
            "platform.config_store",
            "platform.auth"
        ],
        "agent_roles": [
            "admin"
        ]
        }
    }



Best Practices
--------------

1.  Use Roles for Common Permissions

    Create roles for sets of capabilities that multiple agents or groups will need. This reduces duplication
    and makes it easier to maintain consistent permissions across your platform.

2.  Use Groups for Collections of Agents

    When multiple agents need the same permissions, use groups instead of assigning permissions individually.

3. Protect Sensitive Methods in Production Environments

    Service agents' sensitive methods are protected by default, but methods of any installed agent should be protected
    on a case-by-case basis. For example, in a production environment, a driver's write methods that can write values to
    a device should be protected, and only trusted agents should have access to them

4. Use Topic Patterns Consistently

    Use consistent naming schemes for topics to easily protect groups of related topics using patterns. For example:

   .. code-block:: text

       building/<location>/<system>/<sensor>
       building/floor1/hvac/temperature
       building/floor1/lighting/status

   Then protect groups of related topics using patterns.

5. Document Custom Roles

   When creating roles, include comments in the authz.json explaining their purpose and intended use


Authorization vs. Authentication
---------------------------------

**Authentication** answers: "Who are you?"

- Proves identity via credentials (CURVE keys)
- You cannot do anything without authenticating first
- Handled by ``ZMQServerAuthentication``

**Authorization** answers: "What are you allowed to do?"

- Controls access to RPC methods and pub/sub topics
- Only applies after authentication succeeds
- Handled by authorization managers and policies

Example Flow:

1. Agent connects with credentials
2. **Authentication**: Platform verifies credentials match (success → connection allowed)
3. Agent calls RPC method or publishes message
4. **Authorization**: Platform checks if agent has permission for that specific action
5. Action succeeds or fails based on permissions


Advanced Configuration
----------------------

**Role Inheritance**

Roles can be assigned to groups, and groups can have multiple roles:

.. code-block:: json

    {
        "roles": {
            "reader": {
                "pubsub_capabilities": {
                    "historian/query": "subscribe",
                    "historian/results": "subscribe"
                }
            },
            "writer": {
                "rpc_capabilities": [
                    "platform.historian.record"
                ]
            }
        },
        "agent_groups": {
            "data_managers": {
                "identities": ["agent1", "agent2"],
                "agent_roles": ["reader", "writer"]
            }
        }
    }

**Topic Wildcard Examples**

.. code-block:: python

    # All HVAC topics in floor 1
    "building/floor1/hvac/*"

    # All topics in any building
    "*/hvac/temperature"

    # All topics (regex)
    "/.*/

    # Topics matching a complex pattern (regex)
    "/building\\/([^/]+)\\/hvac\\/.*/  # building/*/hvac/...
