#!/bin/bash

echo "This demo will create 2 instances on Nectar, and configure them into a ready-to-run system,
including apache webserver, couchDB server(database, replicator), reletated python dependencies
and harvester."

sleep 10

ansible-playbook -i  host setup.yaml

sleep 90
