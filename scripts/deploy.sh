#!/bin/bash
# scripts/deploy.sh

set -e

# Default values
NAMESPACE="airflow"
ENV="dev"
ACTION="deploy"

# Help function
function show_help {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -n, --namespace NAMESPACE   Kubernetes namespace (default: airflow)"
  echo "  -e, --env ENV               Environment: dev, staging, prod (default: dev)"
  echo "  -a, --action ACTION         Action: deploy, install, upgrade, uninstall, port-forward (default: deploy)"
  echo "  -h, --help                  Show this help"
  exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -n|--namespace)
      NAMESPACE="$2"
      shift 2
      ;;
    -e|--env)
      ENV="$2"
      shift 2
      ;;
    -a|--action)
      ACTION="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      ;;
  esac
done

# Set the environment
export NAMESPACE=$NAMESPACE
export ENV=$ENV

# Execute the make command
echo "Executing: make $ACTION ENV=$ENV NAMESPACE=$NAMESPACE"
make $ACTION ENV=$ENV NAMESPACE=$NAMESPACE