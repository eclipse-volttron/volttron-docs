.. _VIP-Authentication:

==================
VIP Authentication
==================

:ref:`VIP <VIP-Overview>` (VOLTTRON Interconnect Protocol) authentication in modular
VOLTTRON is designed with a clear separation between authentication (proving identity)
and authorization (controlling access). Authentication verifies credentials when a peer
connects, while authorization determines what that authenticated peer can do on the platform.

This document focuses on authentication. For authorization, including capability-based
access control and protected topics, see :ref:`VIP Authorization <VIP-Authorization>`.

Overview
--------

In modular VOLTTRON, authentication is implemented using an extensible framework that:

- Provides a **credentials store** for managing agent and platform credentials
- Supports multiple **authentication mechanisms** (CURVE keys for ZMQ, extensible for others)
- Uses a **message-bus-specific implementation** (e.g., ``ZMQServerAuthentication`` for ZMQ)
- Leverages the **auth service** to coordinate credentials and authentication flows
- Enables **customizable persistence** of credentials

The authentication framework is defined in abstract classes located in ``volttron-core/types/auth/auth_service.py``,
with concrete implementations in ``volttron-lib-auth`` and message-bus-specific implementations
(such as ``volttron-lib-zmq`` for ZMQ).

Architecture
------------

Abstract Classes
~~~~~~~~~~~~~~~~

The authentication framework is built on these abstract base classes defined in ``volttron-core/types/auth/``:

- **Credentials** (base class): Represents a peer's credentials
- **CredentialsStore** (ABC): Interface for storing and retrieving credentials
- **CredentialsCreator** (ABC): Interface for creating new credentials
- **Authenticator** (ABC): Interface for authentication implementations

Concrete Implementations
~~~~~~~~~~~~~~~~~~~~~~~~

**volttron-core** provides abstract interfaces and concrete credential classes:

- **Credentials**: Base class representing a peer's identity (without cryptographic material)
- **PublicCredentials**: Credentials with a public key
- **PKICredentials**: Public key infrastructure credentials (public + secret key)
- **VolttronCredentials**: VOLTTRON-specific PKI credentials extending PKICredentials with domain and address
- **CredentialsFactory**: Factory for creating credentials from various sources
- **DefaultCredentialsFactory** / **DefaultPKICredentialsFactory**: Default credential creators

**volttron-lib-auth** provides the main authentication service:

- **VolttronAuthService**: The main authentication and authorization service that orchestrates credentials and authorization
- Concrete **CredentialsStore** implementation: Persists credentials to disk or other backends
- Custom authentication and authorization manager implementations

**volttron-lib-zmq** provides message-bus-specific implementations:

- **ZMQServerAuthentication**: Handles ZMQ authentication using CURVE mechanism and ZAP protocol
- **ZMQAuthorization**: Handles authorization decisions (protected topics, RPC method access)

Authentication Flow
~~~~~~~~~~~~~~~~~~~

1. **Credential Creation**: When an agent or platform is first configured, credentials
   (e.g., CURVE keypair) are generated and stored
2. **Connection Attempt**: Agent connects with its credentials
3. **ZAP Authentication**: ZMQ's ZAP (ZeroMQ Authentication Protocol) exchanges credentials
4. **Credential Verification**: ``ZMQServerAuthentication.authenticate()`` verifies the credentials
   against the credentials store
5. **Success/Failure**: Authentication succeeds if credentials match; connection is allowed or denied

ZMQ Authentication
------------------

Default Encryption
~~~~~~~~~~~~~~~~~~

By default, ZeroMQ operates in plain-text mode, which is insecure for inter-network communications.
VOLTTRON automatically enables encryption on all TCP connections using `CurveMQ <http://rfc.zeromq.org/spec:26>`__,
which provides elliptic-curve encryption.

Each VOLTTRON platform automatically generates a keypair on startup and uses it for all TCP connections.
To view the platform's public key (used by remote agents to connect):

.. code-block:: bash

    vctl auth servercred

This displays the platform's public key, which remote agents need to know.

Credentials Management
----------------------

Unlike the monolithic VOLTTRON (which used ``auth.json`` with mixed authentication and authorization info),
modular VOLTTRON separates credentials from authorization rules.

**Credentials Storage**

Credentials are stored by the credentials store, by default persisted to disk but can be changed by using a
different AuthzPersistence implementation. Default Credentials used by VOLTTRON ZMQ is VolttronCredentials
that uses a agent's vip identity and public private key pair to authenticate.

Each VolttronCredential entry contains:

- **identity**: The agent or service identifier
- **public_key**: The public part of the credential (shared with peers)
- **private_key**: The private part of the credential (kept secret, only on the platform)
- **mechanism**: Authentication method (e.g., "CURVE" for ZMQ)

**Adding Credentials for Remote Agents**

To allow a remote agent to connect to your platform, you must:

1. Have the remote agent's public key
2. Add it to your platform's credentials store using ``vctl auth add``

Example: Adding a remote agent's credentials:

.. code-block:: bash

    vctl auth add AgentA --publickey HOVXfTspZWcpHQcYT_xGcqypBHzQHTgqEzVb4iXrcDg

This creates a credentials entry for ``AgentA`` with the provided public key. The remote agent
can now authenticate to your platform using its corresponding private key.

**Removing Credentials**

To remove credentials for an agent (preventing it from connecting):

.. code-block:: bash

    vctl auth remove AgentA

**Viewing Agent Credentials**

To view the public keys of all agents on your platform:

.. code-block:: bash

    vctl auth agentcred

Connecting Remote Agents
------------------------

For detailed setup instructions and working examples of connecting remote agents to VOLTTRON instances, see:

- `VOLTTRON Forward Historian <https://github.com/eclipse-volttron/volttron-forward-historian>`__ - Example of an agent connecting to remote VOLTTRON instances
- :ref:`Platform Federation <VIP-Federation>` - For platform-to-platform communication patterns

Platform Configuration
----------------------

The platform binds to VIP addresses to accept connections. By default, it listens only on
the local IPC socket for security. Additional addresses can be configured using the
``--vip-address`` option when starting the platform:

.. code-block:: bash

    volttron -vip ipc:///tmp/volttron-vip tcp://0.0.0.0:22916

This binds to both the local IPC socket and accepts TCP connections from any interface on port 22916.

Each VIP address can include parameters:

- **domain**: A label for this endpoint (defaults to "vip")
- **secretkey**: Alternate private key for this endpoint (defaults to platform's main key)
- **ipv6**: Enable IPv6 support for this endpoint

Example with parameters:

.. code-block:: bash

    volttron -vip tcp://0.0.0.0:22916?domain=external

Authentication vs. Authorization
---------------------------------

**Authentication** answers: "Who are you?"

- Proves identity via credentials (CURVE keys)
- Handled by ``ZMQServerAuthentication``
- Determines if a connection is allowed to be established

**Authorization** answers: "What are you allowed to do?"

- Controls access to RPC methods and pub/sub topics
- Handled by ``ZMQAuthorization``
- Determines what an authenticated peer can do on the platform

In modular VOLTTRON, these are separate concerns with separate configurations.
See :ref:`VIP Authorization <VIP-Authorization-Modular>` for details on controlling
what authenticated agents can access.

Troubleshooting Authentication
-------------------------------

**Connection Timeout: "No response to hello message after 10 seconds"**

This usually means authentication failed. Check:

1. Is the remote agent's public key registered on the platform?

   .. code-block:: bash

       # On the platform
       vctl auth agentcred

2. Does the remote agent have the correct platform public key?

   .. code-block:: bash

       # On the platform
       vctl auth servercred

3. Check platform logs for authentication errors:

   .. code-block:: bash

       # Start platform with verbose logging
       volttron -vv

**"authentication failure" in Logs**

This indicates the presented credentials don't match any known credentials. Verify:

- The public key was added correctly to the credentials store
- No typos in the key (especially if copying manually)
- The key corresponds to the correct agent identity

**Connection Refused**

Check that:

1. The platform is actually listening on the specified address/port
2. Network connectivity exists between the two platforms
3. Firewalls aren't blocking the connection
