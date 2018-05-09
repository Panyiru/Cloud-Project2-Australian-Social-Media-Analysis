#!/bin/bash
python ec2.py
sleep 600


echo setup common softwares on all instances

ansible-playbook -i  host setup.yaml
sleep 60

echo setup webserver
ansible-playbook -i  host webserver.yaml
sleep 60

echo setup dbserver
ansible-playbook -i  host dbserver.yaml
sleep 60

echo install replicators on 3 db servers
ansible-playbook -i  host replication.yaml
sleep 60

echo execute harvesters on 3 db servers
ansible-playbook -i  host execute.yaml
sleep 60
