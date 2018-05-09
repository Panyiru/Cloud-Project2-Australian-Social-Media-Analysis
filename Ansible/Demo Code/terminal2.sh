#!/bin/bash

echo create database and configure replicators between two nodes

ansible-playbook -i host replica.yaml

sleep 90
