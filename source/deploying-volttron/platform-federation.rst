=======================
VOLTTRON Federation
=======================

Overview
========

Federation allows multiple VOLTTRON platforms to securely communicate with each other, enabling cross-platform messaging using publish and subscribe.
This document explains how to set up federation between VOLTTRON platforms, including the REST API endpoints for registration and discovery.

Federation Components
====================

The federation system consists of several components:

- **Federation Registry Service**: An external centralized service that tracks available VOLTTRON platforms
- **Federation Service**: A VOLTTRON platform service that manages connections to other platforms
- **Federation Bridge**: Implements the low-level connection mechanism
- **Routing Service**: Routes messages between local and remote platforms

Setting Up Federation
====================

Start the Federation Registry Service
-------------------------------------

The Federation Registry Service is a critical component that enables platform discovery. It must be set up before configuring individual platforms.

1. Clone the registry service repository:

   .. code-block:: bash

      git clone https://github.com/VOLTTRON/platform-lookup.git
      cd platform-lookup

2. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

3. Start the registry service:

   .. code-block:: bash

      # Default port is 8000 add --port 8080 to specify port 8080
      uvicorn app:app

Enabling Federation
------------------

To enable federation on a VOLTTRON platform, set the appropriate parameters when starting the platform:

.. code-block:: bash

   volttron --enable-federation --address tcp://192.168.1.10:22916 --federation-url http://registry-service:8000

The parameters are:

- ``--enable-federation``: Enables the federation service
- ``--address``: Specifies the external address that other platforms will use to connect
- ``--federation-url``: URL of the federation registry service

Alternatively, update your platform configuration file (VOLTTRON_HOME/config):

.. code-block:: config

   enable_federation = true,
   federation_url = http://registry-service:8000
   address = tcp://192.168.1.10:22916


REST API for Federation Registry
===============================

Registering a Platform
---------------------

When federation is enabled, the federation service of volttron platform automatically registers with the specified registry service.

**Request**:

.. code-block:: http

   POST /platform HTTP/1.1
   Host: registry-service:8000
   Content-Type: application/json

   {
     "id": "platform1",
     "address": "tcp://192.168.1.10:22916",
     "public_credentials": "7Dkj4a...vB3Mm==",
     "group": "default"
   }

**Fields**:

- ``id``: Unique identifier for this platform
- ``address``: External VIP address for other platforms to connect to
- ``public_credentials``: Platform's public key for secure communication
- ``group`` (optional): Group name for categorizing platforms

**Response**:

.. code-block:: http

   HTTP/1.1 201 Created
   Content-Type: application/json

   {
     "id": "platform1",
     "address": "tcp://192.168.1.10:22916",
     "public_credentials": "7Dkj4a...vB3Mm==",
     "group": "default",
     "created_at": "2023-06-24T15:30:22.123456Z"
   }

Discovering Platforms
--------------------

After registration, the federation service periodically queries the registry for other available platforms.

**Request**:

.. code-block:: http

   GET /platforms HTTP/1.1
   Host: registry-service:8000
   Accept: application/json

**Response**:

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   [
     {
       "id": "platform1",
       "address": "tcp://192.168.1.10:22916",
       "public_credentials": "7Dkj4a...vB3Mm==",
       "group": "default"
     },
     {
       "id": "platform2",
       "address": "tcp://192.168.1.11:22916",
       "public_credentials": "9Zkr8b...xF5Nn==",
       "group": "default"
     }
   ]


Federation Connection Process
============================

1. **Registration**: Each platform registers with the federation registry service on startup
2. **Discovery**: Platforms periodically query the registry to discover other platforms
3. **Authentication Setup**: For each discovered platform, credentials are registered with the auth service
4. **Connection Establishment**: A secure connection is established between platforms
5. **Subscription Synchronization**: Topic subscriptions are synchronized between platforms
6. **Message Routing**: Messages are routed between platforms based on subscriptions

Managing Connections
-------------------

The federation service manages connections to other platforms automatically. When a new platform is discovered, a connection is attempted. If a connection fails, the service will retry periodically.

Federation Configuration
=======================

The federation configuration is stored in the VOLTTRON_HOME directory as ``federation_config.json``:

.. code-block:: json

   {
     "platforms": [
       {
         "id": "platform2",
         "address": "tcp://192.168.1.11:22916",
         "public_credentials": "9Zkr8b...xF5Nn==",
         "group": "default",
         "connected": true,
         "last_heartbeat": 1687624821.456
       },
       {
         "id": "platform3",
         "address": "tcp://192.168.1.12:22916",
         "public_credentials": "5Qpn3c...tR7Kk==",
         "group": "default",
         "connected": false,
         "last_heartbeat": 1687624450.123
       }
     ]
   }

Federation Usage Examples
========================

Publishing to a Remote Platform
-----------------------------

Agents can publish messages that will be delivered to subscribers on remote platforms:

.. code-block:: python

   def publish_to_all_platforms(self):
       self.vip.pubsub.publish(
           peer='pubsub',
           topic='global/heartbeat',
           message={'status': 'active', 'timestamp': time.time()}
       )

Subscribing to Remote Topics
--------------------------

Agents can subscribe to topics from other platforms:

.. code-block:: python

   def setup(self):
       # Subscribe to topic from any platform
       self.vip.pubsub.subscribe(
           peer='pubsub',
           prefix='global/heartbeat',
           callback=self.on_heartbeat,
           all_platforms=True  # Subscribe across all federated platforms
       )

   def on_heartbeat(self, peer, sender, bus, topic, headers, message):
       platform_id = headers.get('platform')
       self.vip.pubsub.publish(
           peer='pubsub',
           topic='local/response',
           message={'received_from': platform_id}
       )


Troubleshooting
==============

Common Issues
-----------

1. **Connection Failures**:
   - Verify network connectivity between platforms
   - Check that addresses are externally accessible
   - Ensure public keys are correctly registered

2. **Message Delivery Issues**:
   - Verify topic subscriptions are synchronized
   - Check authorization for cross-platform communication
   - Examine logs for routing errors

Security Considerations
=====================

Federation uses the same security mechanisms as normal VOLTTRON communications:

1. **Authentication**: ZeroMQ CURVE authentication with public/private keys
2. **Encryption**: All communications between platforms are encrypted

To secure federation:

- Use TLS for the federation registry service
- Restrict federation to trusted platforms
- Use strict authorization rules for cross-platform messaging
