#!/bin/bash
set -e

CLUSTER_NAME=$1
echo "Setting up cluster: $CLUSTER_NAME"

# Installation Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Démarrage du cluster
minikube start -p $CLUSTER_NAME --driver=docker --memory=4096
