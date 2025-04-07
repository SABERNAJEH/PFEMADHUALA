#!/bin/bash
set -euo pipefail

CLUSTER_NAME=$1
echo "Initializing cluster: $CLUSTER_NAME"

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start -p "$CLUSTER_NAME" --driver=docker --memory=4096
minikube status
