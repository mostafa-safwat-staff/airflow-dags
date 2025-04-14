# Makefile for airflow-k8s-ops

# Configuration variables
NAMESPACE ?= airflow
RELEASE_NAME ?= airflow
CHART_NAME ?= apache-airflow/airflow
ENV ?= dev
KUBE_CONTEXT ?= $(shell kubectl config current-context)
VALUES_FILE ?= config/airflow-values.yaml
ENV_VALUES_FILE ?= config/values-$(ENV).yaml

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install       - Install Airflow using Helm with values from $(VALUES_FILE)"
	@echo "  upgrade       - Upgrade existing Airflow installation"
	@echo "  uninstall     - Uninstall Airflow"
	@echo "  deploy        - Install or upgrade Airflow (detects which is needed)"
	@echo "  airflow-ui  	- Set up port forwarding to access Airflow UI"
	@echo "  push-image    - Push custom Airflow Docker image"
	@echo "  logs          - Show logs for Airflow components"
	@echo "  lint		   - Check code quality"
	@echo ""
	@echo "Environment variables:"
	@echo "  NAMESPACE     - Kubernetes namespace (default: $(NAMESPACE))"
	@echo "  RELEASE_NAME  - Helm release name (default: $(RELEASE_NAME))"
	@echo "  ENV           - Environment to deploy (dev, staging, prod) (default: $(ENV))"
	@echo "  VALUES_FILE   - Main values file (default: $(VALUES_FILE))"

# Check if Helm release exists
.PHONY: check-release
check-release:
	@if helm status $(RELEASE_NAME) -n $(NAMESPACE) >/dev/null 2>&1; then \
		echo "Release $(RELEASE_NAME) exists"; \
		exit 0; \
	else \
		echo "Release $(RELEASE_NAME) does not exist"; \
		exit 1; \
	fi

# Install Airflow
.PHONY: install
install:
	@echo "Installing Airflow to namespace $(NAMESPACE) with $(VALUES_FILE) and $(ENV_VALUES_FILE)..."
	helm install $(RELEASE_NAME) $(CHART_NAME) \
		--create-namespace \
		--namespace $(NAMESPACE) \
		-f $(VALUES_FILE) \
		-f $(ENV_VALUES_FILE)

# Upgrade Airflow installation
.PHONY: upgrade
upgrade:
	@echo "Upgrading Airflow in namespace $(NAMESPACE) with $(VALUES_FILE) and $(ENV_VALUES_FILE)..."
	helm upgrade $(RELEASE_NAME) $(CHART_NAME) \
		--namespace $(NAMESPACE) \
		-f $(VALUES_FILE) \
		-f $(ENV_VALUES_FILE)

# Uninstall Airflow
.PHONY: uninstall
uninstall:
	@echo "Uninstalling Airflow from namespace $(NAMESPACE)..."
	helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE)

# Deploy (install or upgrade)
.PHONY: deploy
deploy:
	@if helm status $(RELEASE_NAME) -n $(NAMESPACE) >/dev/null 2>&1; then \
		make upgrade; \
	else \
		make install; \
	fi

# Port forward to access Airflow UI
.PHONY: airflow-ui
airflow-ui:
	@echo "Setting up port forwarding to access Airflow UI at http://localhost:8080..."
	kubectl port-forward svc/$(RELEASE_NAME)-webserver 8080:8080 -n $(NAMESPACE)

# Build custom Docker image
.PHONY: push-image
push-image:
	@echo "Building custom Airflow Docker image..."
	docker build -t airflow-custom:latest -f docker/Dockerfile .

	@echo "Pushing custom Airflow Docker image..."
	docker tag airflow-custom:latest msafwat/airflow-custom:latest
	docker push msafwat/airflow-custom:latest

# Show logs for Airflow components
.PHONY: logs
logs:
	@echo "Showing logs for Airflow scheduler..."
	kubectl logs -l component=scheduler -n $(NAMESPACE) --tail=100 -f

# Check code quality
.PHONY: lint
lint:
	@echo "Checking code quality..."
	python -m flake8 dags/*.py || { echo "❌ Lint errors found! See output above."; exit 1; }