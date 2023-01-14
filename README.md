# Bovine

Bovine is attempt at creating a modular ActivityPub server.


### Usage examples

#### Most basic example

By cloning this repository and running
```
DOMAIN=$DOMAIN PYTHONPATH=$PYTHONPATH:$(pwd) hypercorn examples.basic_app:app --bind 0.0.0.0:5000
```
and an appropriate nginx configuration, you obtain an ActivityPub server accepting
all follow requests for the user test.

It also dumps all non accept messages to the inbox
